#!/usr/bin/python     
## -*- coding: utf-8 -*-

import re

from nplus_functions.what_type_of_paragraph import *

def determine_paragraph_types_for_text(text):

    results = []

    paragraphs = re.split('\n\n+', text)
    for p in paragraphs:
        if p.strip() > '':
            if p.startswith('\n') == True:
                results.append([what_type_of_paragraph(p), p[1:]])
            else:
                results.append([what_type_of_paragraph(p), p])
        
    for a in range(1, len(results) - 1):
        if results[a][0] in ['SINGLE', 'ERROR']:
            if results[a - 1][0] == results[a + 1][0]:
                results[a][0] = results[a - 1][0]
                
    return results
