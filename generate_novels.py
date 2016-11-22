#!/usr/bin/python     
## -*- coding: utf-8 -*-

import codecs, json, os.path

from config import *

from nplus_classes.pg_catalog import *
from nplus_classes.digest import *
from nplus_classes.fasttext_results import *
from nplus_classes.author_name import *
from nplus_classes.pg_text import *

from nplus_functions.create_distances_file import *
from nplus_functions.transform_function import *
from nplus_functions.texts_to_pdf_latex import *
from nplus_functions.texts_to_web_latex import *
from nplus_functions.texts_to_pdf_output import *
from nplus_functions.texts_to_web_output import *

if __name__ == "__main__":
    
    pg = PgCatalog(PATH_TO_CATALOG)
    digest = Digest(PATH_TO_DIGEST)
    
    lexicon = json.loads(codecs.open(PATH_TO_LEXICON, 'r', encoding='utf-8').read())

    for a in sorted(pg.catalog):

        if os.path.isfile(PATH_TO_TEXT_OUTPUTS + a['file_name']) == True:
            print 'bypassing -- already transformed', a['author'], a['title'], a['file_name']
        else:
        
            fastext_data = None

            if os.path.isfile(PATH_TO_DISTANCES + a['file_name']) == True:
                print 'bypassing -- distances created', a['author'], a['title'], a['file_name']
                
                fastext_data = FasttextResults(PATH_TO_DISTANCES + a['file_name'])
            else:
                print 'creating distances', a['author'], a['title'], a['file_name']
                
                pg_text = PgText(a['author'], a['title'], PATH_TO_ALL_PG_FILES, PATH_TO_LOCAL_INPUT_FILES, a['file_name'])
                
                create_distances_file(PATH_TO_FASTTEXT_DATA, PATH_TO_DISTANCES + a['file_name'], pg_text.text, a['author'], a['title'])
            
                fastext_data = FasttextResults(PATH_TO_DISTANCES + a['file_name'])
            
            print 'transforming', a['author'], a['title'], a['file_name']
            
            author_name = AuthorName(PATH_TO_AUTHOR_NAME_SUBS, a['author'], fastext_data)

            print author_name.substitutions['new_author_name']

            summary = digest.get_one_summary(a['author'], a['title'])
            pg_text = PgText(a['author'], a['title'], PATH_TO_ALL_PG_FILES, PATH_TO_LOCAL_INPUT_FILES, a['file_name'])

            new_summary, new_pg_text = transform_function(summary, pg_text, author_name, a['title'], fastext_data, lexicon, PATH_TO_SUBSTITUTIONS + a['file_name'].replace('.txt', '.js'), author_name.substitutions['for_text'])

            f = codecs.open(PATH_TO_TEXT_OUTPUTS + a['file_name'].replace('.txt', '_summary.xml'), 'w', encoding='utf-8')
            f.write(new_summary.output_text())
            f.close()

            f = codecs.open(PATH_TO_TEXT_OUTPUTS + a['file_name'], 'w', encoding='utf-8')
            f.write(new_pg_text.output_text())
            f.close()

    for a in sorted(pg.catalog):

        if os.path.isfile(PATH_TO_LATEX_OUTPUTS.replace('../../', '') + a['file_name'].replace('.txt', '.pdf.tex')) == True:
            print 'bypassing -- pdf latex exists', a['author'], a['title'], a['file_name']
        else:
            print 'preparing pdf latex', a['author'], a['title'], a['file_name']
            
            texts_to_pdf_latex(PATH_TO_TEXT_OUTPUTS, a['file_name'], PATH_TO_AUTHOR_NAME_SUBS, PATH_TO_TEMP, PATH_TO_PDF_OUTPUTS, TEMPLATE_FOLDER, PATH_TO_LATEX_OUTPUTS)

    for a in sorted(pg.catalog):

        if os.path.isfile(PATH_TO_LATEX_OUTPUTS + a['file_name'].replace('.txt', '.web.tex')) == True:
            print 'bypassing -- web latex exists', a['author'], a['title'], a['file_name']
        else:
            
            print 'preparing web latex', a['author'], a['title'], a['file_name']
        
            texts_to_web_latex(PATH_TO_TEXT_OUTPUTS, a['file_name'], PATH_TO_AUTHOR_NAME_SUBS, PATH_TO_TEMP, PATH_TO_WEB_OUTPUTS, TEMPLATE_FOLDER, PATH_TO_LATEX_OUTPUTS, URL_FOR_SVG_IMAGES)

    for a in sorted(pg.catalog):

        if os.path.isfile(PATH_TO_PDF_OUTPUTS.replace('../../', '') + a['file_name'].replace('.txt', '.pdf')) == True:
            print 'bypassing -- pdf latex output', a['author'], a['title'], a['file_name']
        else:
            print 'preparing pdf output', a['author'], a['title'], a['file_name']
            
            texts_to_pdf_output(a['file_name'], PATH_TO_TEMP, PATH_TO_PDF_OUTPUTS, PATH_TO_LATEX_OUTPUTS)

    for a in sorted(pg.catalog):

        if os.path.isfile(PATH_TO_WEB_OUTPUTS + a['file_name'].replace('.txt', '.html')) == True:
            print 'bypassing -- web output exists', a['author'], a['title'], a['file_name']
        else:
            
            print 'preparing web output', a['author'], a['title'], a['file_name']
        
            texts_to_web_output(PATH_TO_TEXT_OUTPUTS, a['file_name'], PATH_TO_AUTHOR_NAME_SUBS, PATH_TO_TEMP, PATH_TO_WEB_OUTPUTS, TEMPLATE_FOLDER, PATH_TO_LATEX_OUTPUTS, URL_FOR_SVG_IMAGES, False)
            
