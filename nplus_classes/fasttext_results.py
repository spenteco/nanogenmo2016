#!/usr/bin/python     
## -*- coding: utf-8 -*-

import re, random

from nplus_functions.input_file_handler import *

class FasttextResults():
    
    def __init__(self, path_to_data):
        
        self.path_to_data = path_to_data

        self.fasttext_data = {}

        lines = get_file_text(path_to_data).split('\n')
        for line in lines:
            if line.strip() > '':
                
                cols = line.strip().replace(u'—', '').split('\t')

                if cols[1] == re.sub('[^a-z\_]', '', cols[1]):

                    try:
                        self.fasttext_data[cols[0]].append((float(cols[2]), cols[1]))
                    except KeyError:
                        self.fasttext_data[cols[0]] = [(float(cols[2]), cols[1])]
                        
        #print 'self.fasttext_data.keys()', self.fasttext_data.keys()

    def get_near_words(self, word):

        results = None

        try:
            results = self.fasttext_data[word]
        except KeyError:
            pass
    
        return results

    def get_random_near_word(self, word, rita_lexicon):

        results = None
        
        text_word = word.split('_')[0]
        text_pos = word.split('_')[1]
            
        actual_words = []
        possible_words = []

        try:
            
            actual_words = self.fasttext_data[word]
            
            #print 'word', word, 'actual_words', actual_words
            
            for w in actual_words:
                
                fasttext_word = w[1].split('_')[0]
                fasttext_pos = w[1].split('_')[1]
            
                if text_word.startswith(fasttext_word) == False and fasttext_word.startswith(text_word) == False:
                    possible_words.append(w[1])
        except:
            pass
            
        if len(possible_words) > 0:
            results = random.sample(possible_words, 1)[0]

        #print
        #print 'get_random_near_word ACTUAL', word, results, actual_words
        #print 'get_random_near_word POSSIBLE', word, results, possible_words
    
        return results
