#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Unit tests for Braille translation
    Tests:
        - English translation
        - Greek translation
        - Mix of Greek and English (multi-language) sentences

    All tests include numbers, lowercase and uppercase letters in different combinations.
    Also, wherever applicable Grade 2 translation is tested.

    The tests which include Greek will be done twice:
    On one, greek is considered the main language,
    and on the other english is considered the main language.


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

import unittest
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from six import u
import pybrl as brl

class TranslationTests(unittest.TestCase):
    def test_english_translation(self):
        sentence = "Hello WORLD 123"
        output = brl.translate(sentence, main_language = "english")
        actual_output = [['000001', '110010', '100010', '111000', '111000', '101010'], ['000001', '000001', '010111', '101010', '111010', '111000', '100110'], ['001111', '010000', '011000', '010010']]
        # ⠠⠓⠑⠇⠇⠕ ⠠⠠⠺⠕⠗⠇⠙ ⠼⠂⠆⠒ 
        self.assertEqual(output, actual_output)

    def test_greek_main_translation(self):
        sentence = u"Τεστ 3,5 σουβλακι"
        # Greek is the main language
        output = brl.translate(sentence, main_language = "greek")
        actual_output = [['000101', '011110', '100010', '011100', '011110'], ['001111', '010010', '010001'], ['011100', '101001', '110000', '111000', '100000', '101000', '010100']]
        # ⠨⠞⠑⠎⠞ ⠼⠒⠢ ⠎⠥⠃⠇⠁⠅⠊ 
        self.assertEqual(output, actual_output)

    def test_greek_foreign_translation(self):
        sentence = u"Τεστ 3,5 σουβλακι"
        # English is the main language
        output = brl.translate(sentence, main_language = "english")
        actual_output = [['000010', '000001', '011110', '100010', '011100', '011110'], ['001111', '010010', '010001'], ['000010', '011100', '101001', '110000', '111000', '100000', '101000', '010100']]
        # ⠐⠠⠞⠑⠎⠞ ⠼⠒⠢ ⠐⠎⠥⠃⠇⠁⠅⠊ 
        self.assertEqual(output, actual_output)

    def test_mix_english_with_greek(self):
        sentence = u"English is the main language but let me show my GREEK: Καλημέρα σας! 59310"
        # English is the main language
        output = brl.translate(sentence, main_language = "english")
        actual_output = [['000001', '100010', '101110', '110110', '111000', '010100', '100101'], ['010100', '011100'], ['011101'], ['101100', '100000', '001010'], ['111000', '100000', '101110', '110110', '101001', '100000', '110110', '100010'], ['110000'], ['111000', '100010', '011110'], ['101100', '100010'], ['100101', '010101'], ['101100', '101111'], ['000001', '000001', '110110', '111010', '100010', '100010', '101000'], ['000010', '000001', '101000', '100000', '111000', '001110', '101100', '000010', '000101', '111010', '100000'], ['000010', '011100', '100000'], ['001111', '010001', '001010', '010010', '010000', '001011']]
        # ⠠⠑⠝⠛⠇⠊⠩ ⠊⠎ ⠮ ⠍⠁⠔ ⠇⠁⠝⠛⠥⠁⠛⠑ ⠃ ⠇⠑⠞ ⠍⠑ ⠩⠪ ⠍⠽ ⠠⠠⠛⠗⠑⠑⠅ ⠐⠠⠅⠁⠇⠜⠍⠐⠨⠗⠁ ⠐⠎⠁ ⠼⠢⠔⠒⠂⠴ 
        self.assertEqual(output, actual_output)

    def test_mix_english_with_greek(self):
        sentence = u"Η κύρια γλώσσα είναι τα Ελληνικά. ΑΓΓΛΙΚΆ: Foo bar 59310"
        # Greek is the main language
        output = brl.translate(sentence, main_language = "greek")
        actual_output = [['000101', '001110'], ['101000', '000010', '000101', '111010', '010100', '100000'], ['110110', '111000', '000010', '000100', '011100', '011100', '100000'], ['000010', '000101', '101110', '110001'], ['011110', '100000'], ['000101', '100010', '111000', '111000', '001110', '101110', '010100', '101000', '000010', '000101'], ['000101', '000101', '100000', '110110', '110110', '111000', '010100', '101000', '000010', '000101'], ['000011', '000001', '110100', '101010', '101010'], ['000011', '110000', '001110'], ['001111', '010001', '001010', '010010', '010000', '001011']]
        # ⠨⠜ ⠅⠐⠨⠗⠊⠁ ⠛⠇⠐⠈⠎⠎⠁ ⠐⠨⠝⠣ ⠞⠁ ⠨⠑⠇⠇⠜⠝⠊⠅⠐⠨ ⠨⠨⠁⠛⠛⠇⠊⠅⠐⠨ ⠰⠠⠋⠕⠕ ⠰⠃⠜ ⠼⠢⠔⠒⠂⠴ 
        self.assertEqual(output, actual_output)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TranslationTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
