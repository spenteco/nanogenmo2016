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
from nplus_functions.svg_from_pdf2xml import *
from nplus_functions.colors import *

def texts_to_web_output(text_folder, file_name, author_name_subs_folder, temp_folder, web_folder, template_folder, latex_folder, url_for_svg_images, is_digest):
    
    print 'processing', file_name
    
    f = codecs.open(latex_folder + file_name.replace('.txt', '.web.tex'), 'r', encoding='utf-8')
    final_document = f.read()
    f.close()
    
    execute_command('cd ' + temp_folder + '; pdflatex --halt-on-error ../' + latex_folder.replace('data/', '') + file_name.replace('.txt', '.web.tex'))
    execute_command('cd ' + temp_folder + '; pdftohtml ' + file_name.replace('.txt', '.web.pdf') + ' -xml')
    execute_command('cd ' + web_folder + 'pages/; rm -r ' + file_name.replace('.txt', '') + '; mkdir ' + file_name.replace('.txt', ''))
    
    page_numbers = svg_from_pdf2xml(temp_folder + file_name.replace('.txt', '.web.xml'), web_folder + 'pages/' + file_name.replace('.txt', '') + '/', url_for_svg_images)
    
    extra_page = False
    if len(page_numbers) % 2 == 1:
        extra_page = True
    
    title = None
    new_author_title_page_name = None
    
    if is_digest == True: 
        title = 'Descriptive Catalog\nand\nBibliography\nfor the\nMoMoGenMo Treasury\nof\n N-Plus Literature'
        new_author_title_page_name = 'Stephen M. Pentecost'
    else:
        summary = etree.parse(text_folder + file_name.replace('.txt', '_summary.xml')).getroot()
    
        title = summary.get('print_title').replace('\\n', '\n')
        
        author_name = AuthorName(author_name_subs_folder, summary.get('author'), None)
        new_author_title_page_name = author_name.substitutions['new_author_title_page_name']
    
    title_lines = title.split('\n')
        
    name_lines = []
    name_parts = re.split('\s+', new_author_title_page_name)
    
    if len(name_parts) < 3:
        name_lines = name_parts
    else:
        if len(name_parts) == 3:
            name_lines = [name_parts[0] + ' ' + name_parts[1], name_parts[2]]
        else:
            name_lines = [name_parts[0] + ' ' + name_parts[1], name_parts[2] + ' ' + name_parts[3]]
    
    title_top = 350
    if len(title_lines) == 1:
        title_top = 400
    if len(title_lines) > 3:
        title_top = 325
    
    html_template = Template(filename=template_folder + 'page_flipper.html')
    
    title_font_size = '32px'
    if is_digest == True:
        title_font_size = '24px'
    
    color_number = str(colors[file_name]).rjust(2, '0')
    
    flipper_page = html_template.render(author_top='100', author_lines=name_lines, title_top=str(title_top), title_lines=title_lines, page_numbers=page_numbers, document_id=file_name.replace('.txt', ''), extra_page=extra_page, title_font_size=title_font_size, color_number=color_number)
    
    f = codecs.open(web_folder + file_name.replace('.txt', '.html'), 'w', encoding='utf-8')
    f.write(flipper_page)
    f.close()
    
    #execute_command('cd ' + temp_folder + '; rm ' + file_name.replace('.txt', '.*'))
