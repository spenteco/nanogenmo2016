#!/usr/bin/python     
## -*- coding: utf-8 -*-

import re, codecs, json
from textblob import TextBlob
from nplus_functions.adjust_capitalization import *

class AuthorName():
    
    def __init__(self, path_to_files, original_author_name, fastext_data):
        
        self.original_author_name = original_author_name
        self.file_name = re.sub('\s+', '_', re.sub('[^a-z0-9]', ' ', original_author_name.lower())) + '.json'
        
        self.substitutions = None
        name_exists = False
        try:
            self.substitutions = json.loads(codecs.open(path_to_files + self.file_name, 'r', encoding='utf').read())
            name_exists = True
        except IOError:
            
            self.substitutions = {'original_author_name': self.original_author_name, 'token_subs': {}, 'for_text': {}}

            blob = TextBlob(self.original_author_name)

            for tag in blob.tags:

                word = tag[0]
                pos = 'nnp'
    
                if len(pos) > 1:

                    original_t =  word.lower() + '_' + pos.lower()
                    sub_t = fastext_data.get_random_near_word(original_t, {})

                    if sub_t != None:
                        if word.lower() not in self.substitutions['token_subs']:
                            self.substitutions['token_subs'][word.lower()] = sub_t.split('_')[0]
                            self.substitutions['for_text'][word.lower() + '_' + pos.lower()] = sub_t

            new_tokens = []

            for token in re.split('([^A-Za-z0-9\-])', self.original_author_name):

                sub_word = None

                if len(token) > 1 or token.lower() == 'a':

                    try:
                        a = self.substitutions['token_subs'][token.lower()]
                        if a != None:
                            sub_word = a
                    except KeyError:
                        pass

                if sub_word == None:
                    new_tokens.append(token)
                else:
                    new_tokens.append(adjust_capitalization(token, sub_word))

            self.substitutions['new_author_name'] = ''.join(new_tokens)

            name_parts = self.substitutions['new_author_name'][:self.substitutions['new_author_name'].find(' (')].split(', ')

            self.substitutions['new_author_title_page_name'] = ''

            if len(name_parts) == 1:
                self.substitutions['new_author_title_page_name'] = name_parts[0]
            else:
                if len(name_parts) == 2:
                    self.substitutions['new_author_title_page_name'] = name_parts[1] + ' ' + name_parts[0]
                else:
                    self.substitutions['new_author_title_page_name'] = 'MISSING NAME RULE'

        if name_exists == False:
            f = codecs.open(path_to_files + self.file_name, 'w', encoding='utf')
            f.write(json.dumps(self.substitutions))
            f.close()
