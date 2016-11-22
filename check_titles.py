#!/usr/bin/python     
## -*- coding: utf-8 -*-

import os, re, json, codecs
from config import *
from lxml import etree

if __name__ == "__main__":

    lexicon = json.loads(codecs.open(PATH_TO_LEXICON, 'r', encoding='utf-8').read())

    all_unchanged_words = []

    for file_name in os.listdir(PATH_TO_TEXT_OUTPUTS):

        if file_name.find('_summary.xml') > -1:

            #print 'PROCESSING', file_name

            tree = etree.parse(PATH_TO_TEXT_OUTPUTS + file_name)
            root = tree.getroot()

            old_title = re.sub('\s+', ' ', re.sub('[^A-Za-z0-9]', ' ', root.get('title')).strip())
            new_title = re.sub('\s+', ' ', re.sub('[^A-Za-z0-9]', ' ', root.get('print_title').replace('\\n', '\n')).strip())

            #print old_title, new_title

            if old_title == new_title:
                print 'ERROR' + '\t' + file_name + '\t' + old_title + '\t' + new_title
            else:
                old_title_words = re.split('[^A-Za-z0-9]', old_title.lower())
                new_title_words = re.split('[^A-Za-z0-9]', new_title.lower())
                unchanged_words = []
                for w in old_title_words:
                    if w in new_title_words:

                        pos_list = ['UNK',]
                        try:
                            pos_list = lexicon[w]
                        except KeyError:
                            pass

                        word_is_error = False
                        if len(pos_list) == 1 and pos_list[0] in ['nn', 'nns', 'nnp', 'nnps', 'jj', 'jjr']:
                            word_is_error = True
                        if len(pos_list) == 1 and pos_list[0].startswith('vb') == True:
                            word_is_error = True

                        if word_is_error == True:
                            unchanged_words.append(w)
                            all_unchanged_words.append(w + '_' + str(pos_list))

                if len(unchanged_words) > 0:
                    print 'ERROR' + '\t' + file_name + '\t' + old_title + '\t' + new_title

    #print
    #print sorted(list(set(all_unchanged_words)))
    
