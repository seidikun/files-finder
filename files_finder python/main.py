# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 16:34:59 2019

@author: wap
"""
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, 'Z:\\Tranfers\\seidi\\Lib')

from my_config_folders_list import params
from map_folders import folders_mapper
import notificator as nt
import pandas as pd
import os

"""
Init variables and objects
"""
# Init notificator
_notificator = nt.notificator()

# Program modes
_modes = ['EXIT', 'Mapping Mode (map files in table)', 'Filtering Mode', 'Merge Mode']
_choice_mode = 1

# Init mapper
_fm = folders_mapper()

# Init params
_params = params()

# Create an empty dataframe
files_list = pd.DataFrame()

# All other variables
line_separator = '_'*100

# Ask user for control flags
choice_substring = input('Use substring match in Filtering Mode?(0 NO | 1 YES) ')
if int(choice_substring):
    _params.dict_params['match_substring'] = True

"""
Start state-machine
"""
while _choice_mode:
    print(line_separator)
    count = 0
    for mode in _modes:
        print(count,' - ',mode)
        count += 1
        
    _choice_mode = int(input('Type a number: '))    
    
    # Do mapping
    if _choice_mode == 1:
        print(line_separator + '\nMapping Mode\n')        
        _fm.do_mapping(_params, _notificator)        
    
    # Do filtering
    elif _choice_mode == 2:
        print(line_separator + '\nFiltering Mode\n')
        dir_list = os.listdir()
        if _params.dict_params['list_filename'] not in dir_list:
            print(_params.dict_params['list_filename'] + ' not found in current directory\nDo mapping first!')
            
            print('\nCurrent working folder: ' + os.getcwd())
        else:
            files_list = _fm.do_filtering(_params, _notificator, files_list)
    
    # Do merge
    elif _choice_mode == 3:
        print(line_separator)
    
    elif _choice_mode == 0:
        print('Ok, Exiting!\n')
        
    else:
        print(line_separator + '\nYou typed a non-valid choice!\n')
