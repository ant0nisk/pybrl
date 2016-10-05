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

mathml2variable = {
    """ 
        This Dictionary translates the MathML operation (e.g. mfrac) into the special variable that is used in this module.
        It has some custom indicators, too. (such as mfrac_end)
    """
    'mfrac' : '$fraction_start',
    'mfrac_end' : '$fraction_end',
    'fracline' : '$fraction_line',
    'fracline_diag' : '/',
    'fracshift' : '$fraction_shift',
    'bracketshift' : '$bracket_shift',
#    'mi' : '$id_start',
#    'mo' : '$op_start',
    'mn' : '$number_start',
    'mtext' : '$text_start',
    'mssqrt' : '$sqrt'
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
    
    if not s:
        return ''
    
    brl_output = makeMathList(s)

    return _mathToBrailleHelper(brl_output)

def _mathToBrailleHelper(math_list): #, counters = None); # dbg needs description
    """ 
       
    """
    output_list = [] # One dimensional output ready to be directly translated to Braille
    last_type = ''
    for e in math_list:
        e_type = e[0]
        e_val = e[1]
        
        if e_type == 'mi':                  # Identifiers
            output_list.append(e_val)
        elif e_type == 'mo':                # Operators
            output_list.append(e_val)
        elif e_type == 'mfrac':             # Fractions
            fractionComplexity = detectFractionComplexity(e)
            output_list.extend(['fracshift'] * fractionComplexity)

            output_list.append('mfrac')
            #dbg check for complex and hypercomplex
            #dbg support mixed numbers

            for i in xrange(len(e_val)):
                ch = e_val[i]
                output_list.extend(_mathToBrailleHelper([ch]))
                output_list.extend(['fracshift'] * fractionComplexity)
                if i+1 != len(ch):
                    output_list.append('fracline')

            output_list.extend(['fracshift'] * fractionComplexity)
            output_list.append('mfrac_end')
        elif e_type == 'mn':                # Numbers
            output_list.append(e_val)
        elif e_type == 'mrow':              # Grouped Elements
            output_list.append("(") # dbg add parenthesis shifters if necessary
            output_list.extend(_mathToBrailleHelper(e_val))
            output_list.append(")")

        last_type = e_type # dbg (Add support for this...)
        # dbg add support for: square roots, sqrts with index. Debug the fractions (I think it confuses complex with hyper complex... But that is a Nemeth thing...)

    return output_list

def makeMathList(s):
    """
    Create a structured Dict that can be iterated in such a way, that a structured Braille output can be generated.
    """
    m = parseMathToML(s)
    return xmlToList(m)[1][0][1]

def parseMathToML(s):
    """
    Parse a Mathematic expression from a given string and return an XML Element object.
    """
    parsedMath = asciimathml.parse(s)
    return parsedMath

def detectFractionComplexity(branch_list):
    """
    Detect if a Fraction is Simple, Complex or Hypercomplex. Return values: 0->Simple, 1->Complex, 2->Hypercomplex
    
    The branch_list is of the form [['mfrac', ...]]
        (needs to start with the `mfrac` symbol)
    """
    complexity = 0
    if flattenList(branch_list) == []:
        return 0
    
    for m in xrange(len(branch_list)):
        if branch_list[m] == 'mfrac' and len(branch_list) > m+1:
            for children in branch_list[m+1]:
                if type(children) == list:
                    if children[0] == 'mfrac':
                        complexity += 1
                    elif children[0] == 'mrow':
                        if len(children[1]) == 1 and type(children[1][0]) == list and children[1][0][0] == 'mfrac':
                            complexity += 1
                else:
                    continue
    
        elif branch_list[m] == 'mrow' and len(branch_list) > m+1:
            if len(branch_list[m+1]) == 1 and type(branch_list[m+1][0]) == list and branch_list[m+1][0][0] == 'mfrac':
                complexity += 1

    if complexity > 2: # Never occurs, but let's be sure
        return 2

    return complexity

# [Helper functions and classes below]
#class FileSpoof: # A hacky way to create a file-like object in memory (Used in `mathToBraille`)
#    readDone = False
#    
#    def __init__(self,my_text):
#        self.my_text = my_text
#    
#    def readlines(self):
#        return self.my_text.splitlines()
#    
#    def read(self, b = 999999999999):
#        if self.readDone:
#            return
#        
#        self.readDone = True
#        return self.my_text[:b]

def flattenList(S): # Convert a multi-dimensional list, into 1-dimensional
    if S == []:
        return S
    if isinstance(S[0], list):
        return flattenList(S[0]) + flattenList(S[1:])
    return S[:1] + flattenList(S[1:])

def xmlToList(element): # Convert XML to nested List
    node = [element.tag]
    text = getattr(element, 'text', None)
    if text is not None:
        node.append(text)
    
    child_nodes = []
    for child in element:
        child_nodes.append(xmlToList(child))

    if child_nodes != []:
        node.append(child_nodes)

    return node

#def xmlToDict(element): # Convert XML to nested Dictionaries
#    node = dict()
#
#    text = getattr(element, 'text', None)
#    if text is not None:
#        node['text'] = text
#
#    node.update(element.items())
#
#    child_nodes = {}
#    for child in element:
#        child_nodes.setdefault(child, []).append(xmlToDict(child))
#
#    for key, value in child_nodes.items():
#        if len(value) == 1:
#             child_nodes[key] = value[0]
#
#    node.update(child_nodes.items())
#
#    return node
#
#def normaliseDict(d): # Replaces the keys of the nested dictionaries with the tag names
#    new = {}
#    for k, v in d.iteritems():
#        if isinstance(v, dict):
#            v = normaliseDict(v)
#
#        if type(k) not in [str, unicode]:
#            new[k.tag] = v
#        else:
#            new[k] = v
#
#    return new

## Functions to get/set/delete a dictionary key-value in specific depth in the format rootDict.dict1.dict2.key
## See more: http://stackoverflow.com/a/9320375/1106659
#def get_key(my_dict, key):
#    return reduce(dict.get, key.split("."), my_dict)
#
#def set_key(my_dict, key, value):
#    key = key.split(".")
#    my_dict = reduce(dict.get, key[:-1], my_dict)
#    my_dict[key[-1]] = value
#
#def del_key(my_dict, key):
#    key = key.split(".")
#    my_dict = reduce(dict.get, key[:-1], my_dict)
#    del my_dict[key[-1]]