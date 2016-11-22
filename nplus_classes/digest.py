#!/usr/bin/python     
## -*- coding: utf-8 -*-

import re

from lxml import etree

class Summary():
    
    def __init__(self, summary_node):

        self.summary_node = summary_node

    def get_summary_content(self):
    
        summary_text = []

        for node in self.summary_node.xpath('descendant::text()'):
            summary_text.append(node)

        return re.sub('\s+', ' ', ''.join(summary_text).strip())
        
    def prepare_summary_content(self):
    
        summary_text = []
        title_found = False

        for node in self.summary_node.xpath('descendant::text()'):
            summary_text.append(node)

        for node in self.summary_node.xpath('descendant::*'):
            node.getparent().remove(node)
        
        self.summary_node.text = ''.join(summary_text).strip()

        return self.get_summary_content()

    def output_text(self):

        return etree.tostring(self.summary_node)
        
    def get_sortkey(self):
        
        author_key = self.summary_node.get('new_author_name')
        
        #p = author.find(' (')
        #if p == -1:
        #    name_parts = author.split(', ')
        #else:
        #    name_parts = author[:p].split(', ')
        
        #author_key = ''

        #if len(name_parts) == 1:
        #    author_key = name_parts[0]
        #else:
        #    if len(name_parts) == 2:
        #        author_key = name_parts[0] + ', ' + name_parts[1]
        #    else:
        #        author_key = 'AA MISSING NAME RULE'
        
        title_key = self.summary_node.get('print_title').replace(r'\n', ' ')
        if title_key.lower().startswith('the '):
            title_key = title_key[4:] + ', ' + title_key[:4]
        else:
            if title_key.lower().startswith('a '):
                title_key = title_key[2:] + ', ' + title_key[:2]
            else:
                if title_key.lower().startswith('an '):
                    title_key = title_key[3:] + ', ' + title_key[:3]
        
        return author_key, title_key

    def get_content(self):

        return self.summary_node.text
     
class Digest():
    
    def __init__(self, path_to_digest):
        
        self.path_to_digest = path_to_digest
        self.tree = etree.parse(path_to_digest)
        
    def get_one_summary(self, author, title):
        
        print 'author', author, 'title', title
        
        summaries = self.tree.xpath('//summary[@author="' + author + '" and @title="' + title + '"]')
        
        result = None
        
        if len(summaries) == 1:
            result = Summary(summaries[0])
        else:
            if len(summaries) > 1:
                print 'Digest ERROR', len(summaries), 'summaries found', author, title
            else:
                if len(summaries) == 0:
                    print 'Digest ERROR', 'summary not found', author, title
                    
        return result
