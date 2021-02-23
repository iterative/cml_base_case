# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 14:57:46 2021

@author: Philipe_Leal
"""

import os


def get_parent_dirs(level=1):
    
    parentdir = os.getcwd()
    
    for i in range(level):
        parentdir = os.path.dirname(parentdir)
        
    return parentdir
        