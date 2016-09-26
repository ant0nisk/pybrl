#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Braille Grade 2 Translation
    
    Antonis Katzourakis - @ant0nisktz - inatago.com
"""

from __future__ import unicode_literals
import __builtin__
import os
import types
import languages

use_nemeth_code = True

numbers = { # Order is from 0 to 9
'nemethSystem':
     ['001011',
      '010000',
      '011000',
      '010010',
      '010011',
      '010001',
      '011010',
      '011011',
      '011001',
      '001010'],
'stdSystem':
     ['010110',
      '100000',
      '110000',
      '100100',
      '100110',
      '100010',
      '110100',
      '110110',
      '110010',
      '010100']
}

__builtin__.unicode_literals = unicode_literals

importedAlphabets = {}
importedContractions = {}
importedSpecials = {}
supportedSymbols = {}
_orderedSplitters = []
_Specials = [u'“',u'”',u'$',u'"',u'',u'»',u'«']

def importLanguageFiles(files=[]):
    """ 
    Import the specified language files. If no language files are specified, all them will be imported (Skipping only those with the do_not_import variable set to True)
    """
    global importedAlphabets, importedContractions, importedSpecials, _orderedSplitters
    
    for i in [k for k in dir(languages) if (k in files or k + '.py' in files or files == [])]:
        if (i.startswith("__") and i.endswith("__")) or i == 'os':
            continue
        
        languageModule = eval('languages.{}'.format(i))
        if languageModule.do_not_import == True:
            continue
        else:
            importedAlphabets.update(languageModule.alphabet)
            importedContractions.update(languageModule.contractions)
            importedSpecials.update(languageModule.specialCharacters)

    tmpAlphabets={}
    for k in importedAlphabets: tmpAlphabets[k] = importedAlphabets[k]
    
    importedAlphabets = tmpAlphabets
    upperAlphabets={}
    for k in tmpAlphabets.keys(): upperAlphabets[k.upper()] = tmpAlphabets[k]

    importedAlphabets.update(upperAlphabets)

    _orderedSplitters = importedAlphabets.keys()
    _orderedSplitters = sorted(_orderedSplitters, key=lambda x: len(x.replace("-","")), reverse=True)

def _customIndex(l, element, N=0):
    """
    Custom Index function so that you can find the Nth occurence of an element
    """
    parts = l.split(element, N+1)
    if len(parts) <= N+1:
        return -1
    
    return len(l)-len(parts[-1])-len(element)

def translate(text):
    """
    Translate a text into Braille representation.
    
    - Replaces all the variables
    - Uses the available rules to keep the context straight
    """
    global importedAlphabets, importedContractions, importedSpecials, _orderedSplitters, importedSymbols

    if type(text) != list:
        text = preprocess(text)

    output = []

    for wrd in text:
        outWrd = []
        numberSeries = False
        capitalsStreak = 0
        cntr = 0
        for c in wrd:
            # Digits
            if c.isdigit():
                if numberSeries == False:
                    outWrd.append(importedSpecials['%number'])
                
                numberSeries = True
                if use_nemeth_code:
                    outWrd.append(numbers['nemethSystem'][int(c)])
                else:
                    outWrd.append(numbers['stdSystem'][int(c)])

                continue
            else:
                if numberSeries and c not in languages.mathematics.alphabet:
                    outWrd.append(importedSpecials['%letter'])
            
                numberSeries = False

            # Check for decimal point
            if c == u'.' and numberSeries:
                outWrd.append(importedSpecials['%decimal'])
                continue

            # Non-digit Characters
            if c == u'$':
                outWrd.append(importedSpecials['$dollar'])
                continue
            elif c == u'“' or c == u'«' or c == u'"':
                outWrd.append(importedSpecials['$quote_open'])
                continue
            elif c == u'”' or c == u'»':
                outWrd.append(importedSpecials['$quote_close'])
                continue
            elif c in importedSpecials.keys():
                outWrd.append(importedSpecials[c])
                continue
            
            if not c: # Skip empty characters
                continue
            
            if len(c) > 1: # Is a Prefix, Infix or Suffix
                if cntr == 0:
                    outWrd.append(importedAlphabets[c + "-"]) # Prefix
                elif cntr == len(wrd)-1:
                    outWrd.append(importedAlphabets["-" + c]) # Suffix
                else:
                    outWrd.append(importedAlphabets["-" + c + "-"]) # Infix
            else:
                outWrd.append(importedAlphabets[c])

            cntr += 1

            # Capital Letters
            if c.isupper() and c in importedAlphabets and c not in languages.mathematics.alphabet:
                if capitalsStreak < 2: # If there are two (or more) consecutive capital letters
                    outWrd.insert(len(outWrd) - 1 - capitalsStreak, importedSpecials['%capital'])
                
                if capitalsStreak == 0:
                    capitalsStreak = 1
                else:
                    capitalsStreak = 2
            else:
                if capitalsStreak == 2: # End the Capital letter series
                    outWrd.insert(len(outWrd) - 1, importedSpecials['%capital'])
                    outWrd.insert(len(outWrd) - 1, importedSpecials['%capital'])
                
                capitalsStreak = 0
                
        # Make sure all "characters" are normalized to the valid representation
        normalizedBrl = []
        for brl in outWrd:
            if len(brl) == 6:
                normalizedBrl.append(brl)
            else:
                for i in xrange(len(brl)/6):
                    normalizedBrl.append(brl[i:i+6])

        output.append(normalizedBrl)

    return output

def preprocess(text):
    """
    - Replaces all the available contractions.
    - Split the given text into chunks that can be represented in Braille.
    """
    global importedAlphabets, importedContractions, importedSpecials, _orderedSplitters, importedSymbols

    words = unicode(text, 'utf-8').split(" ")
    output = []
    
    nw = []
    for w in words:
        if w in importedContractions.keys():
            nw.append(importedContractions[w])
        else:
            nw.append(w)

    words = nw
    
    if len(_orderedSplitters) == 0:
        importLanguageFiles()

    for wrd in words:
        w = wrd
        wList = []
        hasEnded = False
        hasStarted = False
        foundCmbs = []
        specialsInsert = {}
        nword = ''
        for i in xrange(len(wrd)):
            char = wrd[i]
            if char.isdigit():
                wList.append(char)
            elif char in importedSpecials.keys() + _Specials:
                specialsInsert[char] = i
                continue
            
            nword += char


        wrd = nword

        for splitter in _orderedSplitters:
            isInfix = False
            isSuffix = False
            isPrefix = False
            
            if splitter.startswith("-"):
                if splitter.endswith("-"):
                    isInfix = True
                else:
                    isSuffix = True
            elif splitter.endswith("-"):
                isPrefix = True

            if isPrefix:
                if wrd.startswith(splitter[:-1]) and w.startswith(splitter[:-1]) and hasStarted == False:
                    foundCmbs.append(splitter[:-1])
                    wList.append(splitter[:-1])
                    w = w[len(splitter[:-1]):]
                    hasStarted = True

            elif isInfix:
                if splitter[1:-1] in w and (not (w.startswith(splitter[1:-1]) and hasStarted)) and (w.endswith(splitter[1:-1]) == False or hasEnded):
                    tmpW = w.split(splitter[1:-1])
                    for k in xrange(len(tmpW) - 1):
                        wList.append(splitter[1:-1])

                    if wrd.startswith(splitter[1:-1]):
                        wList.remove(splitter[1:-1])
                        w = splitter[1:-1] + w.replace(splitter[1:-1], "")
                        foundCmbs.append(splitter[1:-1])
                    else:
                        w = w.replace(splitter[1:-1], "")
            elif isSuffix and hasEnded == False:
                if w.endswith(splitter[1:]):
                    hasEnded = True
                    wList.append(splitter[1:])
                    w = w[:-len(splitter[1:])]
            else:
                if splitter in w:
                    tmp_W = w.split(splitter)
                    w = " ".join(tmp_W)
                    for k in xrange(len(tmp_W) - 1):
                        wList.append(splitter)

        if wList == []:
            if wrd:
                output.append([wrd])
                continue

        orderedSplitWord = {}
        foundLetters = []
        wList = sorted(wList, key=len)
        for cmb in wList:
            foundCmbs.append(cmb)
            kk = str(_customIndex(wrd, cmb, foundCmbs.count(cmb)-1))
            rst = 1
            while kk in orderedSplitWord.keys():
                kk = str(float(kk) - rst + 0.001) # Fix the ordering in some (extremely) rare cases
                rst = 0

            orderedSplitWord[kk] = cmb

        outputWord = [orderedSplitWord[i] for i in sorted(orderedSplitWord.keys(), key=lambda x: float(x))]
        for s in specialsInsert.keys():
            outputWord.insert(specialsInsert[s], s)

        if outputWord != []:
            output.append(outputWord)

    return output