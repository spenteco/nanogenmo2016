#!/usr/bin/python     
## -*- coding: utf-8 -*-

import string, ftfy

from mako.template import Template
from lxml import etree

from nplus_classes.author_name import *

from nplus_functions.determine_paragraph_types_for_text import *
from nplus_functions.tex_escape import *
from nplus_functions.fix_quotes import *
from nplus_functions.fix_small_caps import *
from nplus_functions.execute_command import *

def texts_to_pdf_output(file_name, temp_folder, pdf_folder, latex_folder):
    
    print 'processing', file_name
    
    f = codecs.open(latex_folder + file_name.replace('.txt', '.pdf.tex'), 'r', encoding='utf-8')
    final_document = f.read()
    f.close()
    
    execute_command('cd ' + temp_folder + '; pdflatex --halt-on-error ../' + latex_folder.replace('data/', '') + file_name.replace('.txt', '.pdf.tex'))
    execute_command('cd ' + temp_folder + '; pdfnup ' + file_name.replace('.txt', '.pdf.pdf') + ' --nup 2x1 --outfile ' + pdf_folder + file_name.replace('.txt', '.pdf'))
    execute_command('cd ' + temp_folder + '; rm ' + file_name.replace('.txt', '.*'))
    
