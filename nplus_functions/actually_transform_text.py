#!/usr/bin/python     
## -*- coding: utf-8 -*-

import re

from textblob import TextBlob

from nplus_functions.check_and_correct_pos import *
from nplus_functions.okay_to_transform import *
from nplus_functions.substitutions_to_just_words import *
from nplus_functions.remove_illustration_paragraphs import *

def actually_transform_text(text, original_text, substitutions, fastext_data, rita_lexicon, using_old_substitutions):
    
    if using_old_substitutions == False:

        blob = TextBlob(text)

        for tag in blob.tags:

            word = tag[0].lower()
            pos = tag[1].lower()
            
            pos = check_and_correct_pos(word, pos, rita_lexicon)

            if okay_to_transform(word, pos, tag[0]) == True:
                
                sub_key = word + '_' + pos

                if sub_key not in substitutions:
                    sub = fastext_data.get_random_near_word(sub_key, rita_lexicon)
                    if sub != None:
                        substitutions[sub_key] = [sub, 1]
                    else:
                        substitutions[sub_key] = [None, 1]
                else:
                    substitutions[sub_key][1] += 1 

    sub_words = substitutions_to_just_words(substitutions)
    
    number_words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']

    lines = re.split('(\n)', remove_illustration_paragraphs(original_text))
    
    new_lines = []
   
    for line in lines:
        
        okay_to_change_line = True
        
        if re.match('chapter|the end|contents|scene|act|canto|argument|argument|part|book', line.lower().strip()) != None:
            okay_to_change_line = False
            
        if okay_to_change_line == False:
            new_lines.append(line)
        else:
            
            new_tokens = []

            old_tokens = re.split('([^A-Za-z0-9\-])', line)
            
            for token in old_tokens:
                
                okay_to_change_token = True
                
                if token.lower() in number_words:
                    okay_to_change_token = False
                    
                if token.strip() > '' and re.sub('[ivxclm]', '', token.lower()) == '':
                    okay_to_change_token = False
                    
                try:
                    noop = int(token)
                    okay_to_change_token = False
                except:
                    pass    

                if okay_to_change_token == True:
                    try:
                        new_tokens.append(adjust_capitalization(token, sub_words[token.lower()][0]))
                            
                    except:
                        new_tokens.append(token)
                else:
                    new_tokens.append(token)
                    
            new_lines.append(''.join(new_tokens))
            
    final_tokens = re.split('([^A-Za-z0-9\-])', ''.join(new_lines))
            
    for a, token in enumerate(final_tokens):
        if token.lower() in ['a', 'an']:
            next_word = ''
            b = a + 1
            while b < len(final_tokens):
                if len(final_tokens[b].strip()) > 1:
                    next_word = final_tokens[b]
                    break
                b += 1
            if next_word.lower()[:1] in ['a', 'e', 'i', 'o', 'u']:
                final_tokens[a] = adjust_capitalization(final_tokens[a], 'an')
            else:
                final_tokens[a] = adjust_capitalization(final_tokens[a], 'a')
                
            #print 'A/AN', a, token, next_word, next_word.lower()[:1], b, final_tokens[a]

    return ''.join(final_tokens), substitutions
