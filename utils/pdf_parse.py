#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    PDF Parsing Utilities for Braille

    This module uses PDFMiner by Euske - https://github.com/euske/pdfminer

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
import os

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator

def parsePDF(filepath, password = None):
    # Open and parse a PDF File which is located at filepath.
    # Returns the analysis of each page (with layout)
    if os.path.isfile(filepath) == False:
        raise Exception("PDF File not found")

    fp = open(filepath, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser, password)

    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.
    analysis = []
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        analysis.append(device.get_result())

    return analysis

def extractTextWithLayout(analyzed_data):
    # Simple extraction of text from each page with basic layout support.
    # Sample output object:
    # [
    #     [   # New Page
    #         {   # New Text Group
    #             "text": ["Extracted Text Line 1", "2nd line here"],
    #             "layout": { # This is the box that bounds the text group
    #                 'x0': group.x0,
    #                 'x1': group.x1,
    #                 'y0': group.y0,
    #                 'y1': group.y1
    #             }
    #         }
    #     ]
    # ]    

    data = []
    for page in analyzed_data:
        if page.groups == None:
            continue

        data.append({})
        for group in page.groups:
            data[-1]['text'] = group.get_text().split("\n")
            data[-1]['layout'] = {
                    'x0': group.x0,
                    'x1': group.x1,
                    'y0': group.y0,
                    'y1': group.y1
                }
    return data
