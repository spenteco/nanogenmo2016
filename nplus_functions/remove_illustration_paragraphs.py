#!/usr/bin/python     
## -*- coding: utf-8 -*-

import re

from nplus_functions.adjust_capitalization import *

def remove_illustration_paragraphs(text):
    
    good_paragraphs = []
    
    for p in re.split('\n\n+', text):
        
        is_illustration = False
        
        if p.strip().startswith('[') == True and p.strip().endswith(']') == True:
            if p.lower().find('illustration') > -1 or p.lower().find('picture') > -1:
                is_illustration = True
                
        if is_illustration == False:
            good_paragraphs.append(p)
            
    return '\n\n'.join(good_paragraphs) 
    
