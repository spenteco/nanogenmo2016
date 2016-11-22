#!/usr/bin/python     
## -*- coding: utf-8 -*-

from pyexcel_ods import get_data

class PgCatalog():
    
    def __init__(self, path_to_catalog):
        
        self.catalog = []

        data = get_data(path_to_catalog)
        
        for line in data['Sheet1'][1:]:

            if len(line) > 0:
                
                pg_author = line[0]
                pg_title = line[1]
                file_name = line[2]
                
                self.catalog.append({'author': pg_author, 'title': pg_title, 'file_name': file_name})

    def get_author_and_title(self, file_name):
        
        author = ''
        title = ''
        
        for a in self.catalog:
            if a['file_name'] == file_name:
                author = a['author']
                title = a['title']
                
        return author, title
        
        
