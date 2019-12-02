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
    os.chdir(data_path)
    tmp = next(os.walk('.'))[1]
    extension = 'xlsx'

    for robust_folder in range(0, len(tmp)):
        path = "Robust_" + str(robust_folder)
        os.chdir(path)
        excel_files = [i for i in glob.glob('*.{}'.format(extension))]
        for excel in excel_files:
            out = excel.split('.')[0]+'.csv'
            df = pd.read_excel(excel) # if only the first sheet is needed.
            df.to_csv(out)
            os.remove(excel)
        os.chdir('..')
    os.chdir('..')

#######################################################################
# STEP 2 - To delete the first column from the new csv files, to use only once
#######################################################################
def step_two(data_path):
    extension = 'csv'
    os.chdir(data_path)
    tmp = next(os.walk('.'))[1]
    for robust_folder in range(0, len(tmp)):
        path = "Robust_" + str(robust_folder)
        os.chdir(path)

        excel_files = [i for i in glob.glob('*.{}'.format(extension))]
        for excel in excel_files:
            out = excel.split('.')[0] + '.csv'
            df = pd.read_csv(excel)
            first_column = df.columns[0]

            df = df.drop([first_column], axis=1)
            df.to_csv(out, index=False)
            os.chdir('..')
        os.chdir('..')
