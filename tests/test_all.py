#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Includes all the test modules from this directory 
    and runs the tests.

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

# Load test modules
from test_translate import *
from test_utils import *
from test_math import *

# Load test cases
test_cases = [TranslationTests, UtilitiesTests, MathTests]

# Run the tests
test_loader = unittest.TestLoader()
suites = []
for case in test_cases:
    suite = test_loader.loadTestsFromTestCase(case)
    suites.append(suite)

main_suite = unittest.TestSuite(suites)
runner = unittest.TextTestRunner(verbosity=2)
results = runner.run(main_suite)
