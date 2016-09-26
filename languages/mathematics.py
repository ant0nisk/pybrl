# -*- coding: utf-8 -*-

# Mathematics representation for Braille (Nemeth Code)

from __future__ import unicode_literals
import sympy

do_not_import = False       # Change this if you don't want it imported in the Braille translator


""" NOTICE:
This is a special file which includes representations for Mathematics and special symbols. The alphabet shouldn't contain any letters.

This will be used if the use_nemeth_code is set to True, and only if Math input is detected. Otherwise, the mathematics_std.py will be used.
 """

alphabet = {
    '+' : '010011',
    '-' : '000011',
    '*' : '010000010111',
    '=' : '010001100010',
    '/' : '010010',
    '!' : '111011',
    '(' : '101111',
    ')' : '011111',
    '[' : '010000101111',
    ']' : '010000011111',
    '{' : '010001101111',
    '}' : '010001011111',

}

contractions = {}

specialCharacters = {
    '%letter' : '000101',
    '$decimal' : '010001',
    '$comma' : '000001',
    '$tripple_dot' : '000010000010000010000010',
    '$cross_mult' : '010000100001',
    '$dot_mult' : '100001',
    '$div' : '010001010010',
    '$radicalIndex' : '101001',
    '$sqrt' : '010110',
    '$sqrt_end' : '111101',

}

def constructLaTeX(math_expr, evaluate = False): # Needs work...
    """
    Construct the LaTeX representation of a mathematical expression
    """
    return sympy.latex(sympy.sympify(math_expr, evaluate = evaluate))