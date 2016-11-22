#!/usr/bin/python     
## -*- coding: utf-8 -*-

import re

from nplus_functions.normalize_capitalization import *

def fix_small_caps(s, inject_textsc):

    new_tokens = []

    tokens = re.split('([^A-Za-z0-9])', s)
    for t in tokens:
        if t.isalpha() == True and t.upper() == t:
            if inject_textsc == True:
                new_tokens.append(r'\textsc{' + normalize_capitalization(t) + '}')
            else:
                new_tokens.append(t)
        else:
            new_tokens.append(t)
    
    return ''.join(new_tokens)
    
