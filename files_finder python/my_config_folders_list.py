# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 15:06:53 2019

@author: wap
"""

class params():
    
    def __init__(self):
        dict_params = {}
        dict_params['parent_dirs']   = ['C:\\Users\\wap\\Downloads\\']
        
        # List of subfoldrrs to ignore during mapping mode
        dict_params['exclude_dirs']  = ['']
        
        dict_params['list_filename']   = 'filesList.csv'
        
        dict_params['folder_filtered'] = 'C:\\Users\\wap\\Documents\\GitHub\\files-finder\\files_finder python\\filtered_lists\\'  
        
        dict_params['date_format']     = '%d_%m_%Y'
        
        dict_params['match_substring'] = False       
        
        
        self.dict_params = dict_params
        print('initialized params')