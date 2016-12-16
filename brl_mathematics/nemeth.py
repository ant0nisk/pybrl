# -*- coding: utf-8 -*-

"""
    Nemeth Code for Scientific notation in Braille

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

symbols = {
    '!': '111101',
    '(': '111011',
    ')': '011111',
    '*': '000100001111',
    '+': '001101',
    '-': '001001',
    '/': '000111001100',
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
    '≠': '001100000101101000',
    '%': '000100001011',
    ':': '000111',
    '∠': '110101010101',

    # Greek Alphabet
    'Α': '000000101000001100000',
    'Γ': '000000101000001110110',
    'Β': '000000101000001110000',
    'Ε': '000000101000001100010',
    'Δ': '000000101000001100110',
    'Η': '000000101000001001110',
    'Ζ': '000000101000001101011',
    'Ι': '000000101000001010100',
    'Θ': '000000101000001100111',
    'Λ': '000000101000001111000',
    'Κ': '000000101000001101000',
    'Ν': '000000101000001101110',
    'Μ': '000000101000001101100',
    'Ο': '000000101000001101010',
    'Ξ': '000000101000001101101',
    'Ρ': '000000101000001111010',
    'Π': '000000101000001111100',
    'Σ': '000000101000001011100',
    'Υ': '000000101000001101111',
    'Τ': '000000101000001011110',
    'Χ': '000000101000001110010',
    'Φ': '000000101000001110100',
    'Ω': '000000101000001010110',
    'Ψ': '000000101000001111101',
    'α': '000000101100000',
    'γ': '000000101110110',
    'β': '000000101110000',
    'ε': '000000101100010',
    'δ': '000000101100110',
    'η': '000000101001110',
    'ζ': '000000101101011',
    'ι': '000000101010100',
    'θ': '000000101100111',
    'λ': '000000101111000',
    'κ': '000000101101000',
    'ν': '000000101101110',
    'μ': '000000101101100',
    'ο': '000000101101010',
    'ξ': '000000101101101',
    'ρ': '000000101111010',
    'π': '000000101111100',
    'σ': '000000101011100',
    'υ': '000000101101111',
    'τ': '000000101011110',
    'χ': '000000101110010',
    'φ': '000000101110100',
    'ω': '000000101010110',
    'ψ': '000000101111101'
}

# Notes/Observations:
# (DONE) For Complex fractions just add 000001 before the fraction. If it is hypercomplex, add 2 of these.
# Also holds for enlarged parenthesis and the pipe symbol |. Add this operator to add multiple. If there is a shift operator (000100) add it after that.
#

specialCharacters = {
    '%letter': '000011',
    
    '$comma': '000001',
    '$decimal': '000101',
    '$radicalIndex': '110001',
    '$sqrt': '001110',
    '$sqrt_end': '110111',
    '$tripple_dot': '001000001000001000',


    # dbg complete the dict below:
    '$fraction_shift': '000001',
    '$sqrt_shift': '000001',
    '$bracket_shift': '000100',
    '$fraction_start': '100111',
    '$fraction_end': '001111',
    '$fraction_line': '001100',
    '$number_start': '001111',
    '$text_start': '000011',
    '$separation_line': '010010010010010010',
    '$sub': '000011'        # IMPORTANT NEEDS LOGIC IN __init__
}
