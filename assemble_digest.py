#!/usr/bin/python     
## -*- coding: utf-8 -*-

import sys, os, os.path, commands, re, codecs, string, numpy

from lxml import etree
from mako.template import Template

from config import *
from nplus_classes.digest import *
from nplus_classes.pg_catalog import *
from nplus_functions.what_type_of_paragraph import *
from nplus_functions.fix_digest_paragraph import *
from nplus_functions.execute_command import *
from nplus_functions.texts_to_pdf_output import *
from nplus_functions.texts_to_web_output import *

def summaries_to_tex(document_type):
    
    #   GATHER DATA

    summaries = []

    for file_name in os.listdir(PATH_TO_TEXT_OUTPUTS):
        if file_name.find('_summary.xml') > -1:
            
            root = etree.parse(PATH_TO_TEXT_OUTPUTS + file_name).getroot()
            summaries.append([Summary(root), file_name])
    
    author_keyed_summaries = {}
    title_keyed_summaries = {}
    
    for s in summaries:
        
        author_key, title_key = s[0].get_sortkey()
        
        try:
            noop = author_keyed_summaries[author_key]
        except KeyError:
            author_keyed_summaries[author_key] = {}
            
        author_keyed_summaries[author_key][title_key] = s[1] 
        
        try:
            noop = title_keyed_summaries[title_key]
            print 'ERROR', 'duplicate title', author_key, title_key
        except KeyError:
            title_keyed_summaries[title_key] = s[0]
     
    for t in sorted(title_keyed_summaries.keys()):
        print t
    
    #   LOAD TEMPLATES
        
    document_template = Template(filename=TEMPLATE_FOLDER + 'document.tex')
    blank_page_template = Template(filename=TEMPLATE_FOLDER + 'blank_page.tex')
    title_page_template = Template(filename=TEMPLATE_FOLDER + 'catalog_title_page.tex')
    copyright_template = Template(filename=TEMPLATE_FOLDER + 'catalog_copyright.tex')
    header_and_footer_template = Template(filename=TEMPLATE_FOLDER + 'header_and_footer.tex')
    works_template = Template(filename=TEMPLATE_FOLDER + 'works.tex')
    introduction_template = Template(filename=TEMPLATE_FOLDER + 'introduction.tex')
    
    if document_type == 'web':
        document_template = Template(filename=TEMPLATE_FOLDER + 'web.document.tex')
        header_and_footer_template = Template(filename=TEMPLATE_FOLDER + 'web.header_and_footer.tex')
        title_page_template = Template(filename=TEMPLATE_FOLDER + 'web.catalog_title_page.tex')
        works_template = Template(filename=TEMPLATE_FOLDER + 'web.works.tex')
        introduction_template = Template(filename=TEMPLATE_FOLDER + 'web.introduction.tex')
    
    #   OUTPUT SUMMARIES
    
    tex_body = [r'\newpage',]
    
    tex_body.append(r'\newpage')
    tex_body.append(r'\begin{center}')
    if document_type == 'web':
        tex_body.append(r'\textbf{DESCRIPTIVE CATALOG}')
    else:
        tex_body.append(r'\textbf{\textsc{Descriptive Catalog}}')
    tex_body.append(r'\end{center}')
    
    for l in header_and_footer_template.render(title='Descriptive Catalog', author='Stephen M. Pentecost').split('\n'):
        tex_body.append(l)
            
    print      
    for t in sorted(title_keyed_summaries.keys()):
        for p in re.split('\n\n+', title_keyed_summaries[t].get_content()):
            
            paragraph_type = what_type_of_paragraph(p)
            
            if paragraph_type == 'VERSE':
                
                INDENT_FACTOR = 2
                
                tex_body.append(r'\par')
                tex_body.append(r'\noindent')
                
                lines = p.split('\n')
                
                for line_n, line in enumerate(lines):
                    
                    indent_amount = 0
                    s = re.search('[^\s]', line)
                    if s != None:
                        indent_amount = s.start()
                    indent_string = ''
                    if indent_amount > 0:
                        indent_string = r'\hspace*{' + str(indent_amount * INDENT_FACTOR) + 'mm}'
                    
                    if line_n == len(lines) - 1:
                        tex_body.append(indent_string + fix_digest_paragraph(line, document_type))
                    else:
                        tex_body.append(indent_string + fix_digest_paragraph(line, document_type) + r' \\')
                
            else:
                tex_body.append(r'\par')
                tex_body.append(fix_digest_paragraph(re.sub('\s+', ' ', p), document_type))
    
        tex_body.append(r'\vspace{0.25in}')
    
    #tex_body.append(r'\newpage')
    
    #   OUTPUT BIBLIOGRAPHY
    
    pg = PgCatalog(PATH_TO_CATALOG)
    
    works = []
    
    for a in sorted(author_keyed_summaries.keys()):
        for t in sorted(author_keyed_summaries[a].keys()):
            
            source = author_keyed_summaries[a][t].replace('_summary.xml', '') + '.txt'
            
            pg_author, pg_title = pg.get_author_and_title(source)
            
            works.append(a + '.  ' + r'\textit{' + tex_escape(t.strip()) + '}.  From ' + pg_author + ', ' + r'\textit{' + tex_escape(pg_title) + '} (' + source + ').' + r'\linebreak')

    #   RENDER TEMPLATES
    
    tex_pages = []
    tex_pages.append(blank_page_template.render())
    tex_pages.append(title_page_template.render())
    tex_pages.append(copyright_template.render())
    tex_pages.append(blank_page_template.render())
    tex_pages.append(blank_page_template.render())
    tex_pages.append(introduction_template.render())
    tex_pages.append(blank_page_template.render())
    
    tex_pages.append('\n'.join(tex_body))
    
    tex_pages.append(works_template.render(works=works))
    
    final_document = document_template.render(tex_pages=tex_pages)
    
    return final_document

if __name__ == "__main__":
    
    final_document = summaries_to_tex('pdf')
        
    #   OUTPUT; LATEX --> PDF --> 2 UP
    
    f = codecs.open(PATH_TO_LATEX_OUTPUTS + 'catalog.pdf.tex', 'w', encoding='utf-8')
    f.write(final_document)
    f.close()
    
    texts_to_pdf_output('catalog.txt', PATH_TO_TEMP, PATH_TO_PDF_OUTPUTS, PATH_TO_LATEX_OUTPUTS)
    
    final_document = summaries_to_tex('web')
    
    f = codecs.open(PATH_TO_LATEX_OUTPUTS + 'catalog.web.tex', 'w', encoding='utf-8')
    f.write(final_document)
    f.close()
        
    texts_to_web_output(PATH_TO_TEXT_OUTPUTS, 'catalog.txt', PATH_TO_AUTHOR_NAME_SUBS, PATH_TO_TEMP, PATH_TO_WEB_OUTPUTS, TEMPLATE_FOLDER, PATH_TO_LATEX_OUTPUTS, URL_FOR_SVG_IMAGES, True)
        
        
