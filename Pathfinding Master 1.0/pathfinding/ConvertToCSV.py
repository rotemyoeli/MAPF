# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 08:05:00 2018

@author: rotem
"""
#############################################################################
# import packages
##############################################################################
import pandas as pd
import os
import glob


######################################################################
# STEP 1 - To convert new xlsx files into csv format, to use only once
######################################################################
def step_one(data_path):
    extension = 'xlsx'
    os.chdir(data_path)
    folders = next(os.walk('.'))[1]

    for robust_folder in folders:
        os.chdir(robust_folder)
        files = [i for i in glob.glob('*.{}'.format(extension))]
        for input_file in files:
            out = input_file.split('.')[0]+'.csv'
            df = pd.read_excel(input_file)
            first_column = df.columns[0]
            df = df.drop([first_column], axis=1)
            df.to_csv(out)
            os.remove(input_file)
        os.chdir('..')
    os.chdir('..')

#######################################################################
# STEP 2 - To delete the first column from the new csv files, to use only once
#######################################################################
def step_two(data_path):
    extension = 'csv'
    os.chdir(data_path)
    folders = next(os.walk('.'))[1]

    for robust_folder in folders:
        os.chdir(robust_folder)

        files = [i for i in glob.glob('*.{}'.format(extension))]
        for input_file in files:
            df = pd.read_csv(input_file)
            first_column = df.columns[0]

            df = df.drop([first_column], axis=1)
            df.to_csv(input_file, index=False)
            os.chdir('..')
        os.chdir('..')
