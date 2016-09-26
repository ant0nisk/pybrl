# -*- coding: utf-8 -*-

# Mathematics representation for Braille (Nemeth Code)

from __future__ import unicode_literals
import sympy

do_not_import = False       # Change this if you don't want it imported in the Braille translator


""" NOTICE:
This is a special file which includes representations for Mathematics and special symbols. The alphabet shouldn't contain any letters.

This will be used if the use_nemeth_code is set to True, and only if Math input is detected. Otherwise, the mathematics_std.py will be used.
 """

alphabet = {}

MATH= {
    '!': '111101',
    '(': '111011',
    ')': '011111',
    '*': '000100001111',
    '+': '001101',
    '-': '001001',
    '/': '001100',
    '=': '000101101000',
    '[': '000100111011',
    ']': '000100011111',
    '{': '000101111011',
    '}': '000101011111'
}

contractions = {}
specialCharacters = {}

MspecialCharacters = {
    '$comma': '000001',
    '$cross_mult': '000100100001',
    '$decimal': '000101',
    '$div': '000101001100',
    '$dot_mult': '100001',
    '$radicalIndex': '110001',
    '$sqrt': '001110',
    '$sqrt_end': '110111',
    '$tripple_dot': '001000001000001000',
    '%letter': '000011'
 }

def constructLaTeX(math_expr, evaluate = False): # Needs work...
    """
    Construct the LaTeX representation of a mathematical expression
    """
    return sympy.latex(sympy.sympify(math_expr, evaluate = evaluate))