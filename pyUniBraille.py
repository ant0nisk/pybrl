#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    [ pyUniBraille ]
    
    Antonis Katzourakis - @ant0nisktz - inatago.com


    LICENSE:
    Braille Grade 2 Translation in Python

    Copyright (C) 2016 Antonis Katzourakis

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import unicode_literals
import __builtin__
import os
import types
import languages
import brl_mathematics as mathematics

use_nemeth_code = True

__version__ = 0.1

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
_Specials = [u'“',u'”',u'$',u'"',u'\'',u'»',u'«', '$dollar', '$quote_open', '$quote_close', '$shape', '$emph', '$accent', '$decimal', '$comma', '$triple_dot', '$cross_mult', '$dot_mult', '$div', '$sqrt', '$underline']

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
            importedAlphabets[i] = languageModule.alphabet
            importedContractions[i] = languageModule.contractions
            importedSpecials[i] = languageModule.specialCharacters
    
    upperAlphabets={}
    for l in importedAlphabets.keys():
        if l == 'os': continue

        upperAlphabets[l] = {}
        for k in importedAlphabets[l].keys():
            upperAlphabets[l][k.upper()] = importedAlphabets[l][k]

        importedAlphabets[l].update(upperAlphabets[l])

    _orderedSplitters = [i for j in importedAlphabets.keys() for i in importedAlphabets[j].keys()]
    _orderedSplitters = sorted(_orderedSplitters, key=lambda x: len(x.replace("-","")), reverse=True)

    mathematics = use_nemeth_code

def _customIndex(l, element, N=0):
    """
    Custom Index function so that you can find the Nth occurence of an element
    """
    parts = l.split(element, N+1)
    if len(parts) <= N+1:
        return -1
    
    return len(l)-len(parts[-1])-len(element)

def detectLanguage(wrd, mainLanguage = None,avoidMath = False):
    """
    Detect which of the imported Alphabets to use
    """
    if len(importedAlphabets) == 0:
        importLanguageFiles()


    if mainLanguage == None:
        mainLanguage = importedAlphabets.keys()[0]

    if not wrd:
        return mainLanguage
    
    bestHitRate = -1
    targetAlphabet = mainLanguage
    mathHits = 0
    mainLanguageHits = 0

    for a in importedAlphabets.keys():
        hits = 0
        mathHits = 0
        for c in wrd:
            if c.isdigit():
                mathHits += 1
        
            if c in importedAlphabets[a].keys():
                hits += 1
                if a == mainLanguage:
                    mainLanguageHits += 1

        if hits > bestHitRate:
            bestHitRate = hits
            targetAlphabet = a
#               # dbg
#    if mathHits >= bestHitRate and not avoidMath:
#        targetAlphabet = 'mathematics'
#    elif avoidMath:
#         if mathHits > bestHitRate * 1.5: targetAlphabet = 'mathematics'
    if mainLanguageHits == bestHitRate:
        targetAlphabet = mainLanguage

    return targetAlphabet

def translate(text, mainLanguage = None):
    """
    Translate a text into Braille representation.
    
    - Replaces all the variables
    - Uses the available rules to keep the context straight
    """
    global importedAlphabets, importedContractions, importedSpecials, _orderedSplitters, importedSymbols

    if type(text) != list:
        text = preprocess(text)

    if len(importedAlphabets.keys()) == 0:
        raise Exception("No Language files are imported.")
    
    usedLanguage = mainLanguage
    if mainLanguage == None:
        usedLanguage = importedAlphabets.keys()[0]
        if 'english' in importedAlphabets.keys():
            usedLanguage = 'english'

        mainLanguage = usedLanguage

    output = []
    singleQuoteOpened = False
    doubleQuoteOpened = False

    previousLanguage = usedLanguage
    for wrd in text:
        usedLanguage = detectLanguage(wrd, mainLanguage = mainLanguage)
        enableLanguageIndicator = False

        if usedLanguage != mainLanguage:
            enableLanguageIndicator = True
            previousLanguage = usedLanguage

        outWrd = []
        numberSeries = False
        capitalsStreak = 0
        foreignStreak = 0
        foreignCapitalStreak = False
        isContraction = False
        contractedTxtTitled = False

        if "".join(wrd).lower() in importedContractions[usedLanguage].keys():
            isContraction = True
            contractedTxtTitled = wrd[0].isupper()
            wrd = importedContractions[usedLanguage]["".join(wrd).lower()]
        
        cntr = 0
        for c in wrd:
            # Digits
            if c.isdigit():
                if numberSeries == False:
                    outWrd.append(importedSpecials[usedLanguage]['%number'])
                
                numberSeries = True
                if use_nemeth_code:
                    outWrd.append(numbers['nemethSystem'][int(c)])
                else:
                    outWrd.append(numbers['stdSystem'][int(c)])

                continue
            else:
                if numberSeries and c not in mathematics.symbols:
                    outWrd.append(importedSpecials[usedLanguage]['%letter'])
            
                numberSeries = False

            # Check for decimal point
            if c == u'.' and numberSeries:
                outWrd.append(importedSpecials[usedLanguage]['%decimal'])
                continue

            # Non-digit Characters
            if c == u'$':
                if '$dollar' in importedSpecials[usedLanguage].keys():
                    outWrd.append(importedSpecials[usedLanguage]['$dollar'])
                
                if not isContraction:
                    continue
            elif c.startswith('$'):
                if c in importedSpecials[usedLanguage].keys():
                    outWrd.append(importedSpecials[usedLanguage][c])
                
                if not isContraction:
                    continue
            elif c == '"' or c == '\'':
                if '$single_quote_close' not in importedSpecials[usedLanguage].keys() or '$single_quote_open' not in importedSpecials[usedLanguage].keys():
                    c = '"'

                if c == '\'':
                    if singleQuoteOpened == True:
                        outWrd.append(importedSpecials[usedLanguage]['$single_quote_close'])
                        singleQuoteOpened = False
                    else:
                        singleQuoteOpened = True
                        outWrd.append(importedSpecials[usedLanguage]['$single_quote_open'])
                else:
                    if doubleQuoteOpened == True:
                        if '$quote_close' in importedSpecials[usedLanguage].keys():
                            doubleQuoteOpened = False
                            outWrd.append(importedSpecials[usedLanguage]['$quote_close'])
                    else:
                        if '$quote_open' in importedSpecials[usedLanguage].keys():
                            doubleQuoteOpened = True
                            outWrd.append(importedSpecials[usedLanguage]['$quote_open'])

                if not isContraction:
                    continue
            elif c == u'“' or c == u'«' or c == u'"':
                outWrd.append(importedSpecials[usedLanguage]['$quote_open'])
                if not isContraction:
                    continue
            elif c == u'”' or c == u'»':
                outWrd.append(importedSpecials[usedLanguage]['$quote_close'])
                if not isContraction:
                    continue
            elif c in importedSpecials[usedLanguage].keys():
                outWrd.append(importedSpecials[usedLanguage][c])
                if not isContraction:
                    continue
            
            if not c: # Skip empty characters
                continue
            
            if enableLanguageIndicator:
                if foreignStreak == 0:
                    foreignStreak = 1
                    if "%foreign_indicator" in importedSpecials[usedLanguage].keys():
                        outWrd.append(importedSpecials[mainLanguage]['%foreign_indicator'])
        
            if len(c) > 1 or isContraction:
                if c in importedAlphabets[usedLanguage].keys() or isContraction:
                    try:
                        outWrd.append(importedAlphabets[usedLanguage][c])
                    except:
                        try:
                            outWrd.append(importedSpecials[usedLanguage][c])
                        except:
                            pass # It is probably a quote like the `was` contraction in English, which becomes a quote.
                else: # Is a Prefix, Infix or Suffix
                    if cntr == 0:
                        outWrd.append(importedAlphabets[usedLanguage][c + "-"]) # Prefix
                    elif cntr == len(wrd)-1:
                        outWrd.append(importedAlphabets[usedLanguage]["-" + c]) # Suffix
                    else:
                        outWrd.append(importedAlphabets[usedLanguage]["-" + c + "-"]) # Infix
            else:
                outWrd.append(importedAlphabets[usedLanguage][c])

            cntr += 1

            # Capital Letters
            if (c.isupper() and c in importedAlphabets[usedLanguage] and c not in mathematics.symbols) or contractedTxtTitled:
                prfix = ''
                contractedTxtTitled = False
                if enableLanguageIndicator:
                    foreignCapitalStreak = True
                
                if foreignCapitalStreak and enableLanguageIndicator == False: # Foreign Capital streak ended. Start a new without foreign Characters
                    if capitalsStreak == 2:
                        outWrd.insert(len(outWrd) - 1, importedSpecials[mainLanguage]['%foreign_capital'])
                        outWrd.insert(len(outWrd) - 1, importedSpecials[mainLanguage]['%foreign_capital'])

                    capitalsStreak = 0
                
                if capitalsStreak < 2: # If there are two (or more) consecutive capital letters
                    if enableLanguageIndicator:
                        outWrd.insert(len(outWrd) - 1 - capitalsStreak, importedSpecials[usedLanguage]['%foreign_capital'])
                    else:
                        outWrd.insert(len(outWrd) - 1 - capitalsStreak, importedSpecials[usedLanguage]['%capital'])
                
                if capitalsStreak == 0:
                    capitalsStreak = 1
                else:
                    capitalsStreak = 2
            else:
                if capitalsStreak == 2: # End the Capital letter series
                    if enableLanguageIndicator:
                        outWrd.insert(len(outWrd) - 1, importedSpecials[usedLanguage]['%foreign_capital'])
                        outWrd.insert(len(outWrd) - 1, importedSpecials[usedLanguage]['%foreign_capital'])
                    else:
                        outWrd.insert(len(outWrd) - 1, importedSpecials[usedLanguage]['%capital'])
                        outWrd.insert(len(outWrd) - 1, importedSpecials[usedLanguage]['%capital'])
                
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
    variableInsert = {}
    nw = []

    if len(_orderedSplitters) == 0:
        importLanguageFiles()
    
    for i in xrange(len(words)):
        w = words[i]
        if w in _Specials:
            if w not in variableInsert.keys():
                variableInsert[w] = []
            
            variableInsert[w].append(i)
        else:
            nw.append(w)

    words = nw

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
                if char not in specialsInsert.keys():
                    specialsInsert[char] = []
                
                specialsInsert[char].append(i)
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
            for i in specialsInsert[s]:
                outputWord.insert(i, s)

        if outputWord != []:
            output.append(outputWord)

    for v in variableInsert.keys():
        for i in variableInsert[v]:
            output.insert(i, [v])

    return output
