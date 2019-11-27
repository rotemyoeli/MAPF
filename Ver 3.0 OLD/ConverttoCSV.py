# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 08:05:00 2018

@author: rotem
"""
#############################################################################
# import packages
##############################################################################

import random
import numpy as np
import heapq
import matplotlib.pyplot as plt
import pandas as pd
import os
import glob
import openpyxl as openpyxl
import csv


######################################################################
# STEP 1 - To convert new xlsx files into csv format, to use only once
######################################################################

def step_one():
    path = 'data1\\'
    os.chdir(path)
    tmp = next(os.walk('.'))[1]
    extension = 'xlsx'

    for robust_folder in range(0, len(tmp)):
        path = str(robust_folder) + '\\'
        os.chdir(path)
        excel_files = [i for i in glob.glob('*.{}'.format(extension))]
        for excel in excel_files:
            out = excel.split('.')[0]+'.csv'
            df = pd.read_excel(excel) # if only the first sheet is needed.
            df.to_csv(out)
            os.remove(excel)
        path = '..'
        os.chdir(path)
    path = '..'
    os.chdir(path)

#######################################################################
# STEP 2 - To delete the first column from the new csv files, to use only once
#######################################################################
def step_two():
    path = 'data1\\'
    extension = 'csv'
    os.chdir(path)
    tmp = next(os.walk('.'))[1]
    for robust_folder in range(0, len(tmp)):
        path = str(robust_folder) + '\\'
        os.chdir(path)

        excel_files = [i for i in glob.glob('*.{}'.format(extension))]

        for excel in excel_files:
            out = excel.split('.')[0] + '.csv'
            df = pd.read_csv(excel)
            first_column = df.columns[0]


            df = df.drop([first_column], axis=1)
            df.to_csv(out, index=False)
        path = '..'
        os.chdir(path)
    path = '..'
    os.chdir(path)
