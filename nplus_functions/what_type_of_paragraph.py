#!/usr/bin/python     
## -*- coding: utf-8 -*-

import re, numpy

from nplus_functions.is_heading import *

def what_type_of_paragraph(p):
    
    paragraph_type = ''
    
    lines = p.split('\n')
    
    if len(lines) == 1:
        if is_heading(lines[0]):
            paragraph_type = 'HEADING'
        else:
            paragraph_type = 'SINGLE'
    else:
        
        indents = []
        lengths = []

        for line in lines:
            s = re.search('[^\s]', line)
            if s != None:
                indents.append(s.start())
            lengths.append(len(line.strip()))

        indents = sorted(indents)

        consistent_indent = True
        for a in range(0, len(indents) - 1):
            if indents[a] != indents[a + 1]:
                consistent_indent = False

        consistent_indent_but_one = True
        for a in range(1, len(indents) - 2):
            if indents[a] != indents[a + 1]:
                consistent_indent_but_one = False

        lengths = sorted(lengths)[1:]
        
        #print 'lengths', lengths, 'indents', indents, ('*' + p.strip() + '*')
        
        avg_length = int(numpy.mean(lengths))
        avg_indent = int(numpy.mean(indents))
        
        if consistent_indent == True and avg_length >= 56 and indents[0] == 0:
            paragraph_type = 'PROSE'
        else:
            if avg_length <= 55:
                paragraph_type = 'VERSE'
            else:
                if avg_length >= 56 and avg_indent == 0:
                    paragraph_type = 'PROSE'
                else:
                    if avg_length >= 56 and consistent_indent == True:
                        paragraph_type = 'INDENTED PROSE'
                    else:
                        if avg_length >= 56 and consistent_indent_but_one == True:
                            paragraph_type = 'INDENTED PROSE'
                        else:
                            paragraph_type = 'PRESERVE FORMAT'

    return paragraph_type
