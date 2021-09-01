# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 12:23:17 2021

@author: catal
"""

def loadSQLStatments(file_name):
    """assumes file_name is an accessible .txt file composed of characters and line breaks
    returns a list of strings, each string being a line from the input file
    """
    file = open(file_name)
    file_holder = file.readlines()
    file_holder = [line[:-6] for line in file_holder]
    file.close()
    return file_holder

file = loadSQLStatments("SQL solar system raw insert statements.rtf")
for line in file:
    print(line)
    print("---")