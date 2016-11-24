#!/usr/bin/python     
## -*- coding: utf-8 -*-

import re

from nplus_functions.tex_escape import *

def fix_digest_paragraph(p, document_type):

    fixed_p = tex_escape(p.replace('=', ''))

    for i in range(0, len(fixed_p)):
        if fixed_p[i:i + 1] == '"':
            if i == 0:
                fixed_p = '``' + fixed_p[1:]
            else:
                if fixed_p[i - 1:i] == ' ':
                    fixed_p = fixed_p[:i] + '``' + fixed_p[i + 1:]
        else:
            if fixed_p[i:i + 1] == '\'':
                if i == 0:
                    fixed_p = '`' + fixed_p[1:]
                else:
                    if fixed_p[i - 1:i] == ' ':
                        fixed_p = fixed_p[:i] + '`' + fixed_p[i + 1:]

    fixed_lines = []

    lines = fixed_p.split('\n')

    for line in lines:

        new_tokens = []

        tokens = re.split('([^A-Za-z0-9\-])', line)
        for t in tokens:
            if t.isalpha() == True and t.upper() == t:
                
                normalized_t = t
                if len(normalized_t) > 1:
                    normalized_t = t[:1] + t[1:].lower()
                
                if document_type == 'pdf':
                    new_tokens.append(r'\textsc{' + normalized_t + '}')
                else:
                    new_tokens.append(t)
            else:
                new_tokens.append(t)

        fixed_lines.append(''.join(new_tokens))

    return '\n'.join(fixed_lines)
