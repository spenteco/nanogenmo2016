#!/usr/bin/python     
## -*- coding: utf-8 -*-

import re

def is_heading(line):

    result = False

    all_uppercase_alpha = True

    tokens = re.split('([^A-Za-z0-9\-])', line)
    for t in tokens:
        if t.isalpha() == True:
            if t.upper() != t:
                all_uppercase_alpha = False
    
    if all_uppercase_alpha == True:
        result = True
    else:
        m = re.match('chapter|note|glossary|preface|introductory|introduction', line.lower().strip())
        if m != None:
            result = True

    return result
    
