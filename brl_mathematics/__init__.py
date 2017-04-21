# -*- coding: utf-8 -*-

"""
    Mathematics Utilities for Braille

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
import xml.etree.ElementTree as ET
from collections import defaultdict

import asciimathml
from . import nemeth, universal

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
    'msqrt' : '$sqrt',
    'msqrt_end' : '$sqrt_end',
    'msqrt_shift' : '$sqrt_shift'
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
    s = u(s)
    
    if not s:
        return ''
    
    brl_output = makeMathList(s)

    return _mathToBrailleHelper(brl_output)

def _mathToBrailleHelper(math_list, sqrt_shift=0):
    """ 
    Translates the Nested Lists into 1-Dimensional list ready to be translated to Braille.
    """
    output_list = []

    for e in math_list:
        e_type = e[0]
        try:
            e_val = e[1]
        except:
            continue
            
        if e_type == 'mi':                  # Identifiers
            output_list.append(e_val)
        elif e_type == 'mo':                # Operators
            output_list.append(e_val)
        elif e_type == 'mfrac':             # Fractions
            fractionComplexity = detectFractionComplexity(e)
            output_list.extend(['fracshift'] * fractionComplexity)

            output_list.append('mfrac')
            # TODO support mixed numbers # dbg

            for i in xrange(len(e_val)):
                ch = e_val[i]
                output_list.extend(_mathToBrailleHelper([ch]))
                output_list.extend(['fracshift'] * fractionComplexity)
                if i+1 != len(ch):
                    output_list.append('fracline')

            output_list.append('mfrac_end')
        elif e_type == 'mn':                # Numbers
            output_list.append(e_val)
        elif e_type == 'mrow':              # Grouped Elements
            ## For Enlarged Parentheses or Brackets, see nemeth.py notes.
            output_list.extend(_mathToBrailleHelper(e_val, sqrt_shift=sqrt_shift))
        elif e_type == 'msqrt':
            output_list.extend(['msqrt_shift'] * sqrt_shift)
            ## For radical index, add $radicalIndex and the number/operator before that # dbg
            output_list.append('msqrt')
            output_list.extend(_mathToBrailleHelper(e_val, sqrt_shift=sqrt_shift+1))
            output_list.extend(['msqrt_shift'] * sqrt_shift)
            output_list.append('msqrt_end')
            
    return output_list

def makeMathList(s):
    """
    Create a structured Dict that can be iterated in such a way, that a structured Braille output can be generated.
    """
    m = parseMathToML(s)      # Uses asciimathml and will be deprecated.
    return xmlToList(m)[1][0][1]

def parseMathToML(s):
    """
    Parse a Mathematic expression from a given string and return an XML Element object.
    """
    # TODO: This function should probably be avoided, because Ascii to MathML is usually ambiguous.
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
                            cmpl = detectFractionComplexity(children[1][0])
                            complexity += 1 + cmpl
                else:
                    continue
    
        elif branch_list[m] == 'mrow' and len(branch_list) > m+1:
            if len(branch_list[m+1]) == 1 and type(branch_list[m+1][0]) == list and branch_list[m+1][0][0] == 'mfrac':
                complexity += 1

    if complexity > 2:
        return 2

    return complexity

# [Helper functions and classes below]
def flattenList(S):
    """
    Convert a multi-dimensional list, into 1-dimensional
    """
    if S == []:
        return S
    if isinstance(S[0], list):
        return flattenList(S[0]) + flattenList(S[1:])
    return S[:1] + flattenList(S[1:])

def loadXML(xml_string, normalize = True):
    """
    Load XML from string
    """
    if normalize:
        xml_string = xml_string.replace("\n","  ").replace("  ","")
    
    parser = ET.XMLParser(encoding = 'utf-8')
    return ET.fromstring(xml_string, parser = parser)

def xmlToList(element):
    """
    Convert XML to nested List
    """
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
