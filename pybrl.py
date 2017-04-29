#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    [ pybrl ]
    
    Antonis Katzourakis - @ant0nisktz - antonis.cc


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
import builtins
import os
import sys
import types
from inspect import currentframe, getframeinfo

import six
from six import unichr, iteritems, u
from six.moves import range

import languages
import brl_mathematics as mathematics
import utils

use_nemeth_code = True

__version__ = 0.1
_Logfile = "_exceptions.log"    # Log file for caught exceptions
_ErrorVerbosity = True          # Print out info about the caught exceptions

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

_PYTHON_VERSION = sys.version_info
builtins._PYTHON_VERSION = _PYTHON_VERSION
builtins.unicode_literals = unicode_literals
builtins.u = u
builtins.iteritems = iteritems
builtins.unichr = unichr
builtins.range = range  
builtins.xrange = range

# Python 2 and 3 compatibility
xrange = range
unicode = six.text_type

importedAlphabets = {}
importedContractions = {}
importedSpecials = {}
supportedSymbols = {}
_orderedSplitters = []
_Specials = [u'“',u'”',u'$',u'"',u'\'',u'»',u'«', '$dollar', '$quote_open', '$quote_close', '$shape', '$emph', '$accent', '$decimal', '$comma', '$triple_dot', '$cross_mult', '$dot_mult', '$div', '$sqrt', '$underline']

def importLanguageFiles(files=[]):
    """ 
    Import the specified language files. 
    If no language files are specified, all them will be imported (Skipping only those with the do_not_import variable set to True)
    """
    global importedAlphabets, importedContractions, importedSpecials, _orderedSplitters

    for i in [k for k in dir(languages) if (k in files or k + '.py' in files or files == [])]:
        if (i.startswith("__") and i.endswith("__")) or i == "builtins" or i == 'os':
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

def _logError(error, frame, verbose = None):
    """
    Called if an exception occurs. Logs exception to file, if a log file is specified in the _Logfile global.
    """
    frameinfo = getframeinfo(frame)
    filename = frameinfo.filename
    lineno = frameinfo.lineno

    if verbose is None and _ErrorVerbosity == True:
        verbose = True

    if verbose:
        print("Exception in {}<{}>: {}".format(filename, lineno, error))

    if _Logfile != "":
        with open(_Logfile,'a+') as f:
            f.write("{}<{}> : {}".format(filename, lineno, error))

def detectLanguage(wrd, main_language = None, avoidMath = False):
    """
    Detect which of the imported Alphabets to use
    """
    if len(importedAlphabets) == 0:
        importLanguageFiles()

    if main_language == None:
        main_language = list(importedAlphabets.keys())[0]

    if not wrd:
        return main_language
    
    bestHitRate = -1
    targetAlphabet = main_language
    mathHits = 0
    main_languageHits = 0

    for a in importedAlphabets.keys():
        hits = 0
        mathHits = 0
        for c in wrd:
            if c.isdigit():     # Not a good way to detect mathematical expressions
                mathHits += 1
        
            if c in importedAlphabets[a].keys():
                hits += 1
                if a == main_language:
                    main_languageHits += 1

        if hits > bestHitRate:
            bestHitRate = hits
            targetAlphabet = a
#               # dbg
#    if mathHits >= bestHitRate and not avoidMath:
#        targetAlphabet = 'mathematics'
#    elif avoidMath:
#         if mathHits > bestHitRate * 1.5: targetAlphabet = 'mathematics'
    if main_languageHits == bestHitRate:
        targetAlphabet = main_language

    return targetAlphabet

def translate(text, main_language = None):
    """
    Translate text into Braille.
    
    - Replaces all the variables
    - Uses the available rules to keep the context clear
    """
    global importedAlphabets, importedContractions, importedSpecials, _orderedSplitters, importedSymbols

    if type(text) != list:
        text = preprocess(text)

    if len(importedAlphabets.keys()) == 0:
        raise Exception("No Language files are imported.")
    
    usedLanguage = main_language
    if main_language == None:
        usedLanguage = list(importedAlphabets.keys())[0]
        if 'english' in importedAlphabets.keys():
            usedLanguage = 'english'

        main_language = usedLanguage

    output = []
    singleQuoteOpened = False
    doubleQuoteOpened = False

    previousLanguage = usedLanguage
    for wrd in text:
        usedLanguage = detectLanguage(wrd, main_language = main_language)
        enableLanguageIndicator = False

        if usedLanguage != main_language:
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
            elif c.startswith('$'): # Handle variables
                if c in importedSpecials[usedLanguage].keys():
                    outWrd.append(importedSpecials[usedLanguage][c])
                
                if not isContraction:
                    continue
            elif c == '"' or c == '\'': # Handle quotes
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
            
            if enableLanguageIndicator: # Handle foreign languages
                if foreignStreak == 0:
                    foreignStreak = 1
                    if "%foreign_indicator" in importedSpecials[usedLanguage].keys():
                        outWrd.append(importedSpecials[main_language]['%foreign_indicator'])
        
            if len(c) > 1 or isContraction:
                if c in importedAlphabets[usedLanguage].keys() or isContraction:
                    try:
                        outWrd.append(importedAlphabets[usedLanguage][c])
                    except:
                        try:
                            outWrd.append(importedSpecials[usedLanguage][c])
                        except Exception as err:
                            # It is probably a quote like the `was` contraction in English, which becomes a quote.
                            _logError(err, currentframe())
                else: # Is a Prefix, Infix or Suffix
                    try:
                        if cntr == 0:
                            outWrd.append(importedAlphabets[usedLanguage][c + "-"]) # Prefix
                        elif cntr == len(wrd)-1:
                            outWrd.append(importedAlphabets[usedLanguage]["-" + c]) # Suffix
                        else:
                            outWrd.append(importedAlphabets[usedLanguage]["-" + c + "-"]) # Infix
                    except Exception as err:
                        try:
                            outWrd.extend([importedAlphabets[usedLanguage][i] for i in c])
                            _logError(err, currentframe())
                        except Exception as err2:
                            total_err = "An exception occured while handling exception `{}`. \nError message: {}".format(err, err2)
                            _logError(total_err, currentframe())
                            continue
            else:
                try:
                    outWrd.append(importedAlphabets[usedLanguage][c])
                except Exception as err:
                    _logError(err, currentframe())

            cntr += 1

            # Capital Letters
            if (c.isupper() and c in importedAlphabets[usedLanguage]) or contractedTxtTitled: #  and c not in mathematics.symbols
                prfix = ''
                contractedTxtTitled = False
                if enableLanguageIndicator:
                    foreignCapitalStreak = True
                
                if foreignCapitalStreak and enableLanguageIndicator == False: # Foreign Capital streak ended. Start a new without foreign Characters
                    if capitalsStreak == 2:
                        outWrd.insert(len(outWrd) - 1, importedSpecials[main_language]['%foreign_capital'])
                        outWrd.insert(len(outWrd) - 1, importedSpecials[main_language]['%foreign_capital'])

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
                for i in xrange(len(brl) // 6):
                    normalizedBrl.append(brl[i:i+6])

        output.append(normalizedBrl)

    return output

def toUnicodeSymbols(brl, flatten=False):
    """
     Constructs the Unicode representation of a translated braille sentence.
     If flatten=False, a list is returned in the same format as the input.
     Otherwise, a string is returned with the translated Braille in Unicode.
    """
    retObj=[]
    
    for wrd in brl:
        retObj.append([])
        for ch in wrd:
            binary_repr = int(ch[::-1], 2)
            hex_val = hex(binary_repr)[2:]
            if len(hex_val) == 1: hex_val = "0" + hex_val

            uni_code = "28{}".format(hex_val)
            uni_code = unichr(int(uni_code, 16))
            retObj[-1].append(uni_code)
    
    if flatten:
        flattened_array = []
        for j in retObj:
            for i in j:
                flattened_array.append(i)

            flattened_array.append(" ") # Include a space between two words

        return "".join(flattened_array)

    return retObj

def fromUnicodeSymbols(s):
    """
    Convert a braille string (with unicode symbols) to the representation used
    in this program. Used for debugging and as a tool to integrate the Nemeth code.
    """
    s_ = s.split(" ")
    retObj = []

    for wrd in s_:
        word_repr = []
        for ch in wrd:
            hex_val = hex(ord(ch)).replace("0x", "")
            while(len(hex_val) < 4):
                hex_val = "0" + hex_val

            hex_val = hex_val[2:]

            raise_dot = "{0:b}".format(int(hex_val, 16))[::-1]
            while len(raise_dot) < 6:
                raise_dot += "0"

            word_repr.append(raise_dot)
        
        retObj.append(word_repr)

    return retObj

def preprocess(text):
    """
    - Replaces all the available contractions.
    - Split the given text into chunks that can be represented in Braille.
    """
    global importedAlphabets, importedContractions, importedSpecials, _orderedSplitters, importedSymbols

    words = text;
    if type(words) != unicode:
        words = u(words)

    words = words.split(" ")
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
            elif char in list(importedSpecials.keys()) + _Specials:
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

def translatePDF(filepath, password = None, language = None):
    """
    Parse a PDF file from `filepath` using the pdf_utils module.
    Then translate into Braille and return the result.

    NOTE: The information extraction of the PDF is currently basic (only text and basic layout information).
    """
    analyzed_data = utils.pdf_utils.parsePDF(filepath, password)
    pdf_text = utils.pdf_utils.extractTextWithLayout(analyzed_data)

    translated_obj = [] # Same structure as the `pdf_text` variable
    for page in pdf_text:
        npage = []
        for group in page:
            ngroup = group
            ngroup['text'] = translate(" ".join(ngroup['text']), language)
            npage.append(ngroup)

        translated_obj.append(npage)

    return translated_obj
