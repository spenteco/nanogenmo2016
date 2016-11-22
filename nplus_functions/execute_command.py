#!/usr/bin/python     
## -*- coding: utf-8 -*-

import commands

def execute_command(cmd):

    print cmd

    results = commands.getoutput("export PYTHONIOENCODING=UTF-8; " + cmd)
    
    print results
    
