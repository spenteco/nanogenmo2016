#!/usr/bin/python     
## -*- coding: utf-8 -*-

import re

def normalize_capitalization(s):

    new_tokens = []

    tokens = re.split('([^A-Za-z0-9\-])', s.lower())
    for t in tokens:
        if re.sub('[ivxlcm]', '', t) == '':
            new_tokens.append(t.upper())
        else:
            new_tokens.append(t[:1].upper() + t[1:])

    return ''.join(new_tokens)
    
