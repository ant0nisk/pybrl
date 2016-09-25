#!/usr/bin/env

# Text to Braille Translation

import os
import types
import languages

""" Representation:
    [a,b]
    [c,d]
    [e,f] can be represented as:
    
    abcdef
"""

use_nemeth_code = True

numbers = { # Order: 1-9 and the last is 0
'nemethSystem' : [
        '001000',
        '001010',
        '001100',
        '001101',
        '001001',
        '001110',
        '001111',
        '001011',
        '000110',
        '000111'
],
'stdSystem' :
    [   '100000',
        '101000',
        '110000',
        '110100',
        '100100',
        '111000',
        '111100',
        '101100',
        '011000',
        '011100'
    ]}

importedAlphabets = {}
importedShortcuts = {}
importedSpecials = {}
_orderedSplitters = []

def importRules(rules=[]):
    """ 
    Import the specified rules. If no rules are specified, all them will be imported (Skipping only those with the do_not_import variable set to True)
    """
    global importedAlphabets, importedShortcuts, importedSpecials, _orderedSplitters
    for i in dir(languages):
        if (i.startswith("__") and i.endswith("__")) or i == 'os':
            continue

        languageModule = eval('languages.{}'.format(i))
        if languageModule.do_not_import == True:
            continue
        else:
            importedAlphabets.update(languageModule.alphabet)
            importedShortcuts.update(languageModule.shortcuts)
            importedSpecials.update(languageModule.specialCharacters)

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

def sentenceSplitter(text):
    """
    Split the given text into chunks that can be represented in Braille
    """
    global importedAlphabets, importedShortcuts, importedSpecials, _orderedSplitters
    words = text.split(" ")
    output = []
    
    if len(_orderedSplitters) == 0:
        importRules()

    for wrd in words:
        w = wrd
        wList = []
        hasEnded = False
        foundCmbs = []
        
        for splitter in _orderedSplitters:
            isIntermediate = False
            isEnding = False
            
            if splitter.startswith("-"):
                if splitter.endswith("-"):
                    isIntermediate = True
                else:
                    isEnding = True
        
            if isIntermediate:
                if splitter[1:-1] in w and (w.endswith(splitter[1:-1]) == False or hasEnded):
                    tmpW = w.split(splitter[1:-1])
                    for k in xrange(len(tmpW) - 1):
                        wList.append(splitter[1:-1])

                    if wrd.startswith(splitter[1:-1]):
                        wList.remove(splitter[1:-1])
                        w = splitter[1:-1] + w.replace(splitter[1:-1], "")
                        foundCmbs.append(splitter[1:-1])
                    else:
                        w = w.replace(splitter[1:-1], "")
                    
            elif isEnding and hasEnded == False:
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

        orderedSplitWord = {}
        foundLetters = []
        wList = sorted(wList, key=len)
        for cmb in wList:
            foundCmbs.append(cmb)
            kk = str(_customIndex(wrd, cmb, foundCmbs.count(cmb)-1))
            rst = 1
            while kk in orderedSplitWord.keys():
                kk = str(float(kk) - rst + 0.01)
                rst = 0

            orderedSplitWord[kk] = cmb


        output.append([orderedSplitWord[i] for i in sorted(orderedSplitWord.keys(), key=lambda x: float(x))])

    return output