#!/usr/bin/python     
## -*- coding: utf-8 -*-

import os, re, json
from config import *
from nplus_functions.input_file_handler import *  

if __name__ == "__main__":

    for file_name in os.listdir(PATH_TO_AUTHOR_NAME_SUBS):

        a = json.loads(get_file_text(PATH_TO_AUTHOR_NAME_SUBS + file_name))
        
        if a['original_author_name'] == a['new_author_name']:
            print 'ERROR' + '\t' + 'entire name not changed (A)' + '\t' + file_name
        else:
            
            old_p = a['original_author_name'].find('(')
            new_p = a['new_author_name'].find('(')
            
            if old_p > -1 and new_p > -1:
            
                if a['original_author_name'][:old_p].strip() == a['new_author_name'][:new_p].strip():
                    print 'ERROR' + '\t' + 'entire name not changed (B)' + '\t' + file_name

            old_last_name = re.split('[^A-Za-z]', a['original_author_name'])[0]
            new_last_name = re.split('[^A-Za-z]', a['new_author_name'])[0]

            if old_last_name == new_last_name:
                print 'ERROR' + '\t' + 'last name not changed (c)' + '\t' + file_name
            
            #name_tokens = re.split('\s+', re.sub('[^A-Za-z]', ' ', a['original_author_name']).strip())
            #if len(name_tokens) != len(a['token_subs']):
            #    print 'ERROR', 'incomplete substitution', 'FILE', file_name
        
        if a['new_author_title_page_name'] == 'MISSING NAME RULE':
            print 'ERROR' + '\t' + 'missing name rule' + '\t' + file_name
