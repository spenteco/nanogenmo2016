#!/usr/bin/python     
## -*- coding: utf-8 -*-

import codecs, re

from textblob import TextBlob

from nplus_functions.input_file_handler import *

def create_distances_file(fasttext_data, distance_file, pg_text, author, title):
    
    tokens = {}
    
    for t in re.split('[^A-Za-z0-9\-]', author + ' ' + title + ' ' + pg_text):
        tokens[t.lower()] = 1
        
    f = codecs.open(distance_file, 'w', encoding='utf-8')

    lines = get_file_text(fasttext_data).split('\n')
    for line in lines:
        if line.strip() > '':
            
            cols = line.strip().split('\t')
            
            if cols[0].split('_')[0] in tokens:
                f.write(line + '\n')
                
    f.close()
