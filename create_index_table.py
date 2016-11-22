#!/usr/bin/python     
## -*- coding: utf-8 -*-

import os, re, json
from lxml import etree
from mako.template import Template
from config import *
from nplus_classes.pg_catalog import *
from nplus_functions.input_file_handler import *

def clean_author_name(a):
    
    result = a
    
    p = a.find('(')
    if p > -1:
        result = result[:p].strip()
        
    return result
    
def clean_new_title(a):
    
    result = re.sub(r'\\n', ' ', a)
    return re.sub('\s+', ' ', result).strip()

if __name__ == "__main__":

    pg = PgCatalog(PATH_TO_CATALOG)

    table_rows = []

    for file_name in os.listdir(PATH_TO_TEXT_OUTPUTS):

        if file_name.find('_summary.xml') > -1:

            tree = etree.parse(PATH_TO_TEXT_OUTPUTS + file_name)
            root = tree.getroot()

            new_title = root.get('print_title')
            new_author_name = root.get('new_author_name')
            
            source = file_name.replace('_summary.xml', '')
            
            pg_author, pg_title = pg.get_author_and_title(source + '.txt')
        
            number_of_pages = len(os.listdir(PATH_TO_WEB_OUTPUTS + 'pages/' + source + '/'))

            original_tokens = re.split('[^A-Za-z0-9\-]', get_file_text(PATH_TO_TEXT_OUTPUTS + source + '.txt'))

            subs = json.loads(get_file_text(PATH_TO_SUBSTITUTIONS + source + '.js'))
            
            n_changed = 0
            for word, sub in subs.iteritems():
                if sub[0] != None:
                    n_changed += sub[1]
            
            table_rows.append([clean_author_name(new_author_name), clean_new_title(new_title), str(number_of_pages), str(int((float(n_changed) / float(len(original_tokens))) * 100)), source, clean_author_name(pg_author), pg_title])
            
    table_template = Template(filename=TEMPLATE_FOLDER + 'index_table.html')
    final_document = table_template.render(table_rows=table_rows)
    
    f = codecs.open(PATH_TO_WEB_OUTPUTS + 'index.html', 'w', encoding='utf-8')
    f.write(final_document)
    f.close()
        
