#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Unit tests for utilities in the program
    Tests:
        - Language detection
        
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

import pybrl as brl

class UtilitiesTests(unittest.TestCase):
    def test_language_detection(self):
        english_sentence = u"This is a sentence"
        greek_sentence = u"Αυτή είναι μια πρόταση"
        for w in english_sentence.split():
            output = brl.detectLanguage(w, main_language = "english")
            self.assertTrue(output == 'english')
            output = brl.detectLanguage(w, main_language = "greek")
            self.assertTrue(output == 'english')

        for w in greek_sentence.split():
            output = brl.detectLanguage(w, main_language = "greek")
            self.assertTrue(output == 'greek')
            output = brl.detectLanguage(w, main_language = "english")
            self.assertTrue(output == 'greek')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(UtilitiesTests)
    unittest.TextTestRunner(verbosity = 2).run(suite)
