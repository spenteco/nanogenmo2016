#!/usr/bin/python       
## -*- coding: utf-8 -*-

import codecs

def handle_one_encoding(path_to_file, encoding):

    text = None

    try:
        text = codecs.open(path_to_file, 'r', encoding).read().replace(u'–', ' -- ').replace(u'—', ' -- ').replace('  --  ', ' -- ').replace(u'', '')
    except UnicodeDecodeError:
        pass

    return text

def get_file_text(path_to_file):

    text = None

    all_encodings = ['ascii', 'utf-8', 'iso-8859-1']

    for encoding in all_encodings:
        text = handle_one_encoding(path_to_file, encoding)
        if text != None:
            break

    return text 
