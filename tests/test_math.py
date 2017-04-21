#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Unit tests for mathematics within pybrl
    Tests:
        - conversion of math expressions into simple lists 
          which are ready to be translated.
        - MathML to nested lists conversion.
        
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

# MathML Samples of different parsing complexity
ml_simple = """
<math>
    <mn>2</mn>
    <mo>+</mo>
    <mn>3</mn>
    <mo/>
    <mo>=</mo>
    <mo/>
    <mn>5</mn>
</math>"""   # 2 + 3 = 5

ml_simple_fraction = """
<math>
    <mfrac>
        <mn>1</mn>
        <mn>2</mn>
    </mfrac>
    <mo>+</mo>
    <mn>3</mn>
    <mo/>
    <mo>=</mo>
    <mo/>
    <mn>3</mn>
    <mo>.</mo>
    <mn>5</mn>
</math>"""   # 1/2 + 3 = 3.5

ml_complex_fraction = """
<math>
    <mfrac>
        <mfrac>
            <mn>3</mn>
            <mrow>
                <mn>4</mn>
                <mo>+</mo>
                <mn>5</mn>
            </mrow>
        </mfrac>
        <mrow>
            <mn>2</mn>
            <mo>-</mo>
            <mfrac>
                <mn>5</mn>
                <mn>10</mn>
            </mfrac>
        </mrow>
    </mfrac>
</math>
"""
""" 
     3
   _____
   4 + 5
__________
      5
 2 - ____
      10
"""

class MathTests(unittest.TestCase):
    def test_mathml_to_nested_lists(self):
        ml = brl.mathematics.loadXML(ml_simple_fraction)
        expected_output = ['math', [['mfrac', [['mn', '1'], ['mn', '2']]], ['mo', '+'], ['mn', '3'], ['mo'], ['mo', '='], ['mo'], ['mn', '3'], ['mo', '.'], ['mn', '5']]]
        converted_output = brl.mathematics.xmlToList(ml)
        self.assertEqual(converted_output, expected_output)

    def test_simple_math_expression(self):
        # MathML String -> ML XML
        ml = brl.mathematics.loadXML(ml_simple)
        # ML XML -> Nested List
        math_lst = brl.mathematics.xmlToList(ml)
        # Nested List -> List of simple representations ready for Braille translation
        converted_output = brl.mathematics._mathToBrailleHelper(math_lst[1])
        expected_output = ['2', '+', '3', '=', '5']
        self.assertEqual(converted_output, expected_output)

    def test_simple_fraction(self):
        ml = brl.mathematics.loadXML(ml_simple_fraction)
        math_lst = brl.mathematics.xmlToList(ml)
        converted_output = brl.mathematics._mathToBrailleHelper(math_lst[1])
        expected_output = ['mfrac', '1', 'fracline', '2', 'mfrac_end', '+', '3', '=', '3', '.', '5']
        self.assertEqual(converted_output, expected_output)

    def test_complex_fraction(self):
        ml = brl.mathematics.loadXML(ml_complex_fraction)
        math_lst = brl.mathematics.xmlToList(ml)
        converted_output = brl.mathematics._mathToBrailleHelper(math_lst[1])
        expected_output = ['fracshift', 'mfrac', 'mfrac', '3', 'fracline', '4', '+', '5', 'mfrac_end', 'fracshift', 'fracline', '2', '-', 'mfrac', '5', 'fracline', '10', 'mfrac_end', 'fracshift', 'mfrac_end']
        self.assertEqual(converted_output, expected_output)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MathTests)
    unittest.TextTestRunner(verbosity=2).run(suite)

