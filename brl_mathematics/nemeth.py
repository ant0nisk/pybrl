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
    '}': '000101011111'
}

specialCharacters = {
    '%letter': '000011',
    
    '$comma': '000001',
    '$cross_mult': '000100100001',
    '$decimal': '000101',
    '$div': '000101001100',
    '$dot_mult': '100001',
    '$radicalIndex': '110001',
    '$sqrt': '001110',
    '$sqrt_end': '110111',
    '$tripple_dot': '001000001000001000'
}