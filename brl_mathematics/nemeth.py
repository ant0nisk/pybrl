# -*- coding: utf-8 -*-

# Nemeth Code for Scientific notation in Braille
from __future__ import unicode_literals

symbols = {
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
    '}': '000101011111',
    '±': '001101001001',
    '⨯': '000100100001',
    '∙': '100001',
    '÷': '000101001100',
    '∪': '000101001101',
    '∩': '000101100101',
    '|': '110011',
    '←': '110101010101010010010010',
    '→': '110101101010',
    '↑': '110101110001010010010010101010',
    '↓': '110101100101010010010010101010',
    '↔': '110101010101010010010010101010',

}

# Notes/Observations:
# For Complex fractions just add 000001 before the fraction. If it is hypercomplex, add 2 of these.
# Also holds for parenthesis and the pipe symbol |. Add this operator to add multiple. If there is a shift operator (000100) add it after that.
#

specialCharacters = {
    '%letter': '000011',
    
    '$comma': '000001',
    '$decimal': '000101',
    '$radicalIndex': '110001',
    '$sqrt': '001110',
    '$sqrt_end': '110111',
    '$tripple_dot': '001000001000001000'
}