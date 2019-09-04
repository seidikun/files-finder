# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 15:06:53 2019

@author: wap
"""

class params():
    
    def __init__(self):
        dict_params = {}
        dict_params['parent_dirs']   = ['C:\\WAP_DATA', 'Z:\\', 'Y:\\' ,'X:\\']
        
        # List of subfoldrrs to ignore during mapping mode
        dict_params['exclude_dirs']  = ['MRI DATA', 'boost_1_60_0', 'MRI', 'mri', 'Lokomat_data', '.git', 'Multcomp',
                                  'improve_class_acc', 'boost_1_55_0', 'eeglab13_4_4b', 'eeglab14_1_2b', 'eeglab13_1_1b',
                                  'PCAN', 'gtk', 'pkg_offline', 'convertTXTtoXLSX', 'BCILAB-1.1', 'exe.win-amd64-3.6',
                                  'couch4mat-gh-pages']
        
        dict_params['list_filename']   = 'filesList.csv'
        
        dict_params['folder_filtered'] = 'Z:\\WAP_DATA_ANAL\\Organizational\\Files Finder\\files_finder python\\filtered_lists\\'  
        
        dict_params['date_format']     = '%d_%m_%Y'
        
        dict_params['match_substring'] = False       
        
        
        self.dict_params = dict_params
        print('initialized params')