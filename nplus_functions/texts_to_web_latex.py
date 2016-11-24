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

def texts_to_web_latex(text_folder, file_name, author_name_subs_folder, temp_folder, web_folder, template_folder, latex_folder, url_for_svg_images):
    
    print 'processing', file_name
    
    #   TEMPLATES
    
    document_template = Template(filename=template_folder + 'web.document.tex')
    blank_page_template = Template(filename=template_folder + 'blank_page.tex')
    title_page_template = Template(filename=template_folder + 'web.title_page.tex')
    copyright_template = Template(filename=template_folder + 'copyright.tex')
    header_and_footer_template = Template(filename=template_folder + 'web.header_and_footer.tex')
    
    #   TITLE PAGE DATA
    
    summary = etree.parse(text_folder + file_name.replace('.txt', '_summary.xml')).getroot()
    
    author_name = AuthorName(author_name_subs_folder, summary.get('author'), None)
    
    title = summary.get('print_title').replace('\\n', '\n')
    title_lines = title.split('\n')
    
    vspace_setting = 1.0
    if len(title_lines) == 1:
        vspace_setting = 20.0
    if len(title_lines) == 2:
        vspace_setting = 10.0
    
    title_for_tex = []
    for a in title_lines:
        title_for_tex.append(a)
        title_for_tex.append(r'\linebreak')
        title_for_tex.append(r'\linebreak')
        
    lines_after_byline = []
    n_extra_lines = 0
    if len(title_lines) == 1:
        n_extra_lines = 3
    if len(title_lines) == 2:
        n_extra_lines = 2
    if len(title_lines) == 3:
        n_extra_lines = 1
    #else:
    #    if len(title_lines) > 3:
    #        n_extra_lines = 0
    for a in range(0, n_extra_lines):
        lines_after_byline.append(r'\linebreak')
        
    #   DOCUMENT BODY
    
    text = codecs.open(text_folder + file_name, 'r', encoding='utf-8').read()
    
    tex_body = [r'\newpage', r'\pagenumbering{arabic}', r'\pagestyle{fancy}', r'\fancyhf{}']

    header_title = title_lines[0]
    if len(title_lines) > 1:
        if title_lines[0][-1] in string.punctuation:
            header_title = title_lines[0][:-1]

    for l in header_and_footer_template.render(title=header_title, author=author_name.substitutions['new_author_title_page_name']).split('\n'):
        tex_body.append(l)

    paragraphs = determine_paragraph_types_for_text(text)

    INDENT_FACTOR = 2

    for p in paragraphs:
        if p[1].strip() > '':
            
            fixed_p = tex_escape(fix_quotes(ftfy.fix_text(p[1])))
            
            lines = []
            for l in fixed_p.split('\n'):
                if l.strip() > '':
                    lines.append(l)
            
            if p[0] in ['PRESERVE FORMAT', 'VERSE']:
                
                tex_body.append(r'\par')
                tex_body.append(r'\noindent')
                
                for line_n, line in enumerate(lines):
                    
                    indent_amount = 0
                    s = re.search('[^\s]', line)
                    if s != None:
                        indent_amount = s.start()
                    indent_string = ''
                    if indent_amount > 0:
                        indent_string = r'\hspace*{' + str(indent_amount * INDENT_FACTOR) + 'mm}'
                    
                    if line_n == len(lines) - 1:
                        tex_body.append(indent_string + fix_small_caps(line, False))
                    else:
                        tex_body.append(indent_string + fix_small_caps(line, False) + r' \\')
                
            else:
                if p[0] in ['INDENTED PROSE', 'PROSE', 'SINGLE']:
                    
                    indent_amount = 0
                    s = re.search('[^\s]', lines[0])
                    if s != None:
                        indent_amount = s.start()
                        
                    if indent_amount > 0:
                        tex_body.append(r'\begin{adjustwidth}{' + str(indent_amount * INDENT_FACTOR) + 'mm}{}')
                    
                    p_text = re.sub('\s+', ' ', fixed_p.strip())
                    
                    tex_body.append(r'\par')
                    tex_body.append(fix_small_caps(p_text, False))
                        
                    if indent_amount > 0:
                        tex_body.append(r'\end{adjustwidth}')
                    
                else:
                    if p[0] in ['HEADING']:
                                
                        tex_body.append(r'\begin{center}')
                        
                        tex_body.append(fix_small_caps(fixed_p, False))
                    
                        tex_body.append(r'\end{center}')
                        
                    else:
                
                        tex_body.append(r'\par')
                        tex_body.append(r'\noindent')
                        
                        for line_n, line in enumerate(lines):
                            
                            indent_amount = 0
                            s = re.search('[^\s]', line)
                            if s != None:
                                indent_amount = s.start()
                            indent_string = ''
                            if indent_amount > 0:
                                indent_string = r'\hspace*{' + str(indent_amount * INDENT_FACTOR) + 'mm}'
                            
                            if line_n == len(lines) - 1:
                                tex_body.append(indent_string + fix_small_caps(line, False))
                            else:
                                tex_body.append(indent_string + fix_small_caps(line, False) + r' \\')
    
    tex_body.append(r'\newpage')

    #   RENDER TEMPLATES
    
    tex_pages = []
    tex_pages.append(blank_page_template.render(),)
    tex_pages.append(title_page_template.render(vspace_setting=vspace_setting, title='\n'.join(title_for_tex), author=author_name.substitutions['new_author_title_page_name'], lines_after_byline='\n'.join(lines_after_byline)),)
    tex_pages.append(copyright_template.render(original_title=summary.get('title'), original_author=summary.get('author')),)
    tex_pages.append(blank_page_template.render(),)
    tex_pages.append(blank_page_template.render(),)
    
    tex_pages.append('\n'.join(tex_body))
    
    final_document = document_template.render(tex_pages=tex_pages)
        
    #   OUTPUT; LATEX --> PDF --> 2 UP
    
    f = codecs.open(latex_folder + file_name.replace('.txt', '.web.tex'), 'w', encoding='utf-8')
    f.write(final_document)
    f.close()
