# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 15:48:33 2019

@author: wap
"""

import os
from os import listdir
from os.path import isfile, join
import time
import pandas as pd
from datetime import datetime

class folders_mapper():
    
    def __init__(self):
        print('initialized folders_mapper')
        
    def do_mapping(self, params, notificator):
        
        t = time.time()
        notificator.send_msg('Started mapping folders')
        files_list = []   
        exclude_dirs = params.dict_params['exclude_dirs']
        parent_dirs  = params.dict_params['parent_dirs']
        csv_filename = params.dict_params['list_filename']
        dir_count  = 0
        file_count = 0
        
        for folder in parent_dirs:
            #Set listing start location
            start_path = folder
        
            #Traverse directory tree with os.walk()
            # path is the current folder
            # dirs is a list of subfolders
            # files is a list of files
            for (path,dirs,files) in os.walk(start_path):
                print('Directory: {:s}'.format(path))
                dirs[:] = [d for d in dirs if d not in exclude_dirs]
                
                dir_count += 1
                #Repeat for each file in directory
                for file in files:
                    dict_file = {}
                    fstat = os.stat(os.path.join(path,file))
                    
                    mtime = time.strftime("%X %x", time.gmtime(fstat.st_mtime))
                    
                    split_file = file.split('.')
                    if len(split_file) > 1 and len(split_file[-1]) < 6:
                        dict_file['extension'] = split_file[-1]
                    else:            
                        dict_file['extension'] = 'no extension'
                        
                    dict_file['path']      = path
                    dict_file['filename']  = file
                    dict_file['size']      = fstat.st_size
                    dict_file['time']      = mtime
                    dict_file['tag']       = ''
                    dict_file['comments']  = ''
                    dict_file['dup_flag']  = ''
                    files_list.append(dict_file)
                
                    file_count += 1  
        
        df_files_list = pd.DataFrame(files_list) 
        
        # Find duplicates
        print('\nFinding Duplicates')
        duplicates = df_files_list[df_files_list.duplicated(['size', 'filename'])]
        ind_duplicates = duplicates.index
        for i in ind_duplicates:
            df_files_list.loc[i,('dup_flag')] = 'duplicate' 
            
        g   = df_files_list.groupby(['filename', 'size'])
        df1 = df_files_list.set_index(['filename', 'size'])
        df1.index.map(lambda ind: g.indices[ind][0])
        df_files_list['dup_index'] = df1.index.map(lambda ind: g.indices[ind][0])   
        
        df_files_list.to_csv(csv_filename) 
        
         # Print total files and directory count
        print('\nFound {} files in {} directories.'.format(file_count,dir_count))  
        print('It seems that {} files are duplicates'.format(len(duplicates)))  
        
        elapsed = time.time() - t
        msg = 'Finished mapping folders in {:.2f} seconds'.format(elapsed)
        notificator.send_msg(msg)
        
    def do_filtering(self, params, notificator, files_list):        
        
        count = 0
        path = params.dict_params['folder_filtered']
        dir_files = [f for f in listdir(path) if isfile(join(path, f))]
        date_stamp = '%s' % (datetime.now().strftime(params.dict_params['date_format'] ))
        csv_filename = 'filtered_list_' + date_stamp + '_' + str(count) + '.csv'
        while csv_filename in dir_files:
            count += 1
            csv_filename = 'filtered_list_' + date_stamp + '_' + str(count) + '.csv'
        txt_file = open(params.dict_params['folder_filtered'] + csv_filename.replace('csv','txt'), "w")        
        
        if files_list.empty:       
            print('Reading ' + params.dict_params['list_filename'])
            files_list = pd.read_csv(params.dict_params['list_filename'], delimiter = ';')
            print(files_list.columns)
        else:
            choice_read = int(input('Read from filesList.csv? (0 NO | 1 YES) '))
            if choice_read:
                print('Reading ' + params.dict_params['list_filename'])
                files_list = pd.read_csv(params.dict_params['list_filename'], delimiter = ';')
                
        params.dict_params['extensions'] = list(set(files_list.extension))
        params.dict_params['extensions'].sort()
                
        # Filter by parent folder
        inds_folders = self.aux_choose_items(params, 'folders', files_list, txt_file)        
        print()
        print('\n',file=txt_file)
        
        # Filter by extension
        inds_extensions = self.aux_choose_items(params, 'extensions', files_list, txt_file)      
        print()
        print('\n',file=txt_file)        
        
        inds_chosen = list(set(inds_folders) & set(inds_extensions))
        
        # Filter by substring in filename
        if params.dict_params['match_substring']:
            substring      = input('Type substring match (regex): ')
            inds_substring = self.aux_choose_items2(params,substring, files_list, txt_file)
            inds_chosen = list(set(inds_chosen) & set(inds_substring))
            
        # Create a filtered_list from files_list, given inds_chosen
        filtered_list = files_list.iloc[inds_chosen]   
            
        filtered_list.to_csv(params.dict_params['folder_filtered'] + csv_filename)
        msg = csv_filename + ' Saved on ' + params.dict_params['folder_filtered']
        print(msg)
        notificator.send_msg(msg)
        txt_file.close()
        
        return files_list        
    
    # Auxiliary functions
    def aux_choose_items(self, params, type_choice, files_list, txt_file):
        if type_choice == 'folders':
            field_dict = 'parent_dirs'
            field_list = 'path'
        elif type_choice == 'extensions':
            field_dict = 'extensions'     
            field_list = 'extension'       
            
        print('The following ' + type_choice + ' were found:')
        count = 1
        for item in params.dict_params[field_dict]:
            print('\t{:<3d} - {}'.format(count, item))
            count += 1
        choice_items = input('Type a choice of ' + type_choice + '(x, or 0 for all): ')
        
        if choice_items == '0':
            inds_choice = list(range(len(files_list)))
            print('You choose all')
            print('Chosen ' + type_choice + ' (ALL): ',file=txt_file)
            for item in params.dict_params[field_dict]:
                print('\t' + item,file=txt_file)
            
        else:                
            inds_choice = []
            choice_items_split = choice_items.split(',')
            msg = 'Chosen ' + type_choice + ': '
            print(msg)
            print(msg, file=txt_file)
            for number in choice_items_split:
                ind = int(number) - 1 
                corresponding_item = params.dict_params[field_dict][ind]
                msg = '\t' + corresponding_item
                print(msg)                
                print(msg, file=txt_file)
                inds_curr_choice = files_list[field_list].str.contains(corresponding_item.replace('\\','\\\\'))                
                inds_choice.extend([i for i in inds_curr_choice.index if inds_curr_choice[i]])
            
        return inds_choice
        
    def aux_choose_items2(self, params, substring, files_list, txt_file):
        
        print('Substring match:\n\t' + substring,file=txt_file)
        inds_substring = files_list['filename'].str.contains(substring, regex = True)
        return [i for i in inds_substring.index if inds_substring[i]]
        
        
        
            