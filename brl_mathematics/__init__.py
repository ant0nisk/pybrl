# -*- coding: utf-8 -*-

# Mathematics representation for Braille

from __future__ import unicode_literals
import nemeth, universal
import asciimathml
import xml.etree.ElementTree
from collections import defaultdict

"""
This is a special module which includes representations for Mathematics and special symbols in Nemeth code.

This will be used if the use_nemeth_code is set to True, and only if Math input is detected. Otherwise, the `brl_mathematics.universal` module will be used.
 """

symbols= {}

specialCharacters = {}

use_nemeth_code = True
mathModule = None

mathml2variable = { # Translates the MathML operation (e.g. mfrac) into the special variable that is used in this module
    'mfrac' : '$fraction_start',
    'mi' : '$id_start',
    'mo' : '$op_start',
    'mn' : '$number_start',
    'mtext' : '$text_start'
}

def initialize():
    """
    Load the Symbols and Special Characters from the selected module. Default is Nemeth.
    """
    global mathModule, use_nemeth_code, symbols, specialCharacters

    if use_nemeth_code:
        symbols = nemeth.symbols
        specialCharacters = nemeth.specialCharacters
    else:
        symbols = universal.symbols
        specialCharacters = universal.specialCharacters

initialize()

def mathToBraille(s):
    """
    Translate a Math expression in a string to Braille.
    """
    if type(s) != unicode:
        s = unicode(s, 'utf-8')
    
    brl_output = makeDictMath(s)

    return brl_output

def makeDictMath(s):
    """
    Create a structured Dict that can be iterated in such a way, that a structured Braille output can be generated.
    """
    m = parseMathToML(s)
    m = xml.etree.ElementTree.tostring(m)
    f = FileSpoof(m)
    dict_output = []
    skp = False
    keyStack = []
    
    for e,t in xml.etree.ElementTree.iterparse(f, events=("start", "end")):
        if t.tag in ['mstyle', 'math', 'mrow']:
            continue
        
        if skp:
            skp = False
            continue
        else:
            skp = True

        if e == 'start' and dict_output != [] and t.text == None:
            keyStack.append(t.tag)
            dict_output.append({t.tag: []})
        elif e == 'end' and t.text == None:
            keyStack.pop(-1)

        if keyStack == []:
            dict_output.append({t.tag: t.text})
        else:
            currentValue = get_key(dict_output[len(dict_output)-1], ".".join(keyStack))
            if currentValue and currentValue != [None]:
                set_key(dict_output[len(dict_output)-1], ".".join(keyStack), get_key(dict_output[len(dict_output)-1], ".".join(keyStack)) + [t.text])
            else:
                set_key(dict_output[len(dict_output)-1], ".".join(keyStack), [t.text])

    return dict_output

def parseMathToML(s):
    """
    Parse a Mathematic expression from a given string and return an XML Element object.
    """
    parsedMath = asciimathml.parse(s)
    return parsedMath

# [Helper functions/classes below]
class FileSpoof: # A hacky way to create a file-like object in memory (Used in `mathToBraille`)
    readDone = False
    
    def __init__(self,my_text):
        self.my_text = my_text
    
    def readlines(self):
        return self.my_text.splitlines()
    
    def read(self, b = 999999999999):
        if self.readDone:
            return
        
        self.readDone = True
        return self.my_text[:b]

def traverse(o, tree_types=(list, tuple)): #Create a generator to iterate recursively in a list
    if isinstance(o, tree_types):
        for value in o:
            for subvalue in traverse(value, tree_types):
                yield subvalue
    else:
        yield o

# Functions to get/set/delete a dictionary key-value in specific depth in the format rootDict.dict1.dict2.key
# See more: http://stackoverflow.com/a/9320375/1106659
def get_key(my_dict, key):
    return reduce(dict.get, key.split("."), my_dict)

def set_key(my_dict, key, value):
    key = key.split(".")
    my_dict = reduce(dict.get, key[:-1], my_dict)
    my_dict[key[-1]] = value

def del_key(my_dict, key):
    key = key.split(".")
    my_dict = reduce(dict.get, key[:-1], my_dict)
    del my_dict[key[-1]]