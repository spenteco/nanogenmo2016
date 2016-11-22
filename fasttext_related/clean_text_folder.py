#!/usr/bin/python     
## -*- coding: utf-8 -*-

import codecs, re, sys, os, random
from input_file_handler import *
from textblob import TextBlob

N_WORDS_REQUESTED = int(sys.argv[3])

f = codecs.open(sys.argv[2], 'w', encoding='utf-8')

files_in_folder = os.listdir(sys.argv[1])
random.shuffle(files_in_folder)

n_words_output = 0

for file_name in files_in_folder:

    text = get_file_text(sys.argv[1] + file_name)

    blob = TextBlob(text)
    output = []
    for tag in blob.tags:
        output.append('_'.join(tag).lower())

    f.write(' '.join(output) + ' ')

    n_words_output = n_words_output + len(output)
    if n_words_output > N_WORDS_REQUESTED:
        break

f.close()
