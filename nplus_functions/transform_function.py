#!/usr/bin/python     
## -*- coding: utf-8 -*-

import copy, codecs, json

from nplus_functions.actually_transform_text import *

def transform_function(original_summary, original_pg_text, author_name, title, fastext_data, rita_lexicon, path_to_substitutions, author_substitutions):

    summary = copy.deepcopy(original_summary)
    pg_text = copy.deepcopy(original_pg_text)

    substitutions = {}
    for k, v in author_substitutions.iteritems():
        substitutions[k] = [v, 1]
    
    using_old_substitutions = False
    try:
        substitutions = json.loads(codecs.open(path_to_substitutions, 'r', encoding='utf-8').read())
        using_old_substitutions = True
        print path_to_substitutions, 'loaded old substitutions'
    except IOError:
        print path_to_substitutions, 'creating new substitutions'

    #   TEXT

    new_pg_text, substitutions = actually_transform_text(pg_text.text, pg_text.text, substitutions, fastext_data, rita_lexicon, using_old_substitutions)

    pg_text.text = new_pg_text

    #   SUMMARY

    new_title, substitutions, = actually_transform_text(summary.summary_node.get('print_title'), summary.summary_node.get('print_title'), substitutions, fastext_data, rita_lexicon, using_old_substitutions)
    
    summary.summary_node.set('print_title', new_title)

    summary.summary_node.set('new_author_name', author_name.substitutions['new_author_name'])

    new_summary_text, substitutions, = actually_transform_text(summary.prepare_summary_content(), summary.summary_node.text, substitutions, fastext_data, rita_lexicon, using_old_substitutions)
    
    summary.summary_node.text = new_summary_text
    
    #   OUTPUT
    
    f = codecs.open(path_to_substitutions, 'w', encoding='utf-8')
    f.write(json.dumps(substitutions, sort_keys=True, indent=4))
    f.close()
    
    return summary, pg_text

