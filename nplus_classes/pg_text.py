#!/usr/bin/python     
## -*- coding: utf-8 -*-

from shutil import copyfile
from nplus_functions.input_file_handler import *

class PgText():
    
    def __init__(self, author, title, path_to_all_pg_files, path_to_local_input_files, file_name):

        self.author = author
        self.title = title
        self.file_name = file_name
        
        self.text = self.read_file(path_to_local_input_files + file_name)
        
        if self.text == None:
            try:
                print 'copying'
                copyfile(path_to_all_pg_files + file_name, path_to_local_input_files + file_name)
                self.text = self.read_file(path_to_local_input_files + file_name)
            except IOError:
                pass
        
        self.is_valid_and_useful = True
        if self.text == None:
             self.is_valid_and_useful = False
        
    def read_file(self, path_to_file):
        
        result = None
        
        try:
            result = get_file_text(path_to_file)
        except IOError:
            pass
            
        return result

    def output_text(self):

        return self.text
        
