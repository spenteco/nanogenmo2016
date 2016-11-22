#!/usr/bin/python     
## -*- coding: utf-8 -*-

import re

def tex_escape(text):
    """
        :param text: a plain text message
        :return: the message escaped to appear correctly in LaTeX
    """
    # ORIGINALLY FROM http://stackoverflow.com/questions/16259923/how-can-i-escape-latex-special-characters-inside-django-templates, BUT WITH LOTS OF CHANGES
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'(',
        '}': r')',
        '[': r'(',
        ']': r')',
        '~': r'--',
        '^': r'\^{}',
        '\\': r'--',
        '<': r'',
        '>': r'',
        '=': r'',
    }
    regex = re.compile('|'.join(re.escape(unicode(key)) for key in sorted(conv.keys(), key = lambda item: - len(item))))
    return regex.sub(lambda match: conv[match.group()], text)
    
