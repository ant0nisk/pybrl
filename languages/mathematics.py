# -*- coding: utf-8 -*-

# Mathematics representation for Braille

do_not_import = False       # Change this if you don't want it imported in the Braille translator


""" This is a special file which includes representations for Mathematics and special symbols. The alphabet shouldn't contain any letters. """

alphabet = {
    '+' : '000101001110'
}

contractions = {}

specialCharacters = {
    '%letter' : '000101',
    '$decimal' : '001000',
    ',' : '000010'
}