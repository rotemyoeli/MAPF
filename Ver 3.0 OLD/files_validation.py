import heapq
import random
import numpy as np
import heapq
import matplotlib.pyplot as plt
import pandas as pd
import os
import glob
import openpyxl as openpyxl
import csv
import ast
import utils
from tkinter import filedialog
from tkinter import *
import config
import itertools as itert

def load_map():
    map_file_name = e1.get()
    data_folder = e2.get()
    # load the map file into numpy array
    with open(map_file_name, 'rt') as infile:
        grid1 = np.array([list(line.strip()) for line in infile.readlines()])
    print('Grid shape', grid1.shape)

    grid1[grid1 == '@'] = 1  # object on the map
    grid1[grid1 == 'T'] = 1  # object on the map
    grid1[grid1 == '.'] = 0  # free on map

    grid = np.array(grid1.astype(np.int))
    return (grid)


##############################################################################
# Check the output routes validation
##############################################################################
def check_route_validation():
    map_grid = load_map()

    path = 'data1\\'
    extension = 'csv'
    os.chdir(path)
    tmp = next(os.walk('.'))[1]
    for robust_folder in range(0, len(tmp)):

        print('Robust Factor', robust_folder)
        path = str(robust_folder) + '\\'
        os.chdir(path)

        excel_files = [i for i in glob.glob('*.{}'.format(extension))]

        for file in excel_files:
            main_route = []
            with open(file, 'rt') as csvfile:
                # creating a csv reader object
                csvreader = csv.reader(csvfile)
                header = next(csvreader)
                # extracting each data row one by one
                for row in csvreader:
                    tmp_route = []
                    for y in range(0, len(row)):
                        if row[y]:
                            tmp_route.append(ast.literal_eval(row[y]))
                    main_route.append(tmp_route)

                ####################################################
                # Check the validation
                ####################################################
                max_len = 0
                for find_length in range(0, len(main_route)):
                    if len(main_route[find_length]) > max_len:
                        max_len = len(main_route[find_length])

                for num_of_agent in range(0, len(main_route)):
                    for current_step in range(0, len(main_route[num_of_agent])):
                        radius = []
                        radius = utils.get_radius(map_grid, main_route[num_of_agent][current_step][0], robust_folder)
                        for agent_checked in range(0, len(main_route)):
                            if agent_checked != num_of_agent:
                                if len(main_route[num_of_agent]) > current_step and len(main_route[agent_checked]) > current_step+robust_folder:
                                    if len(radius) > 0:
                                        for radius_check in range(0, len(radius)):
                                            if main_route[agent_checked][current_step][0] == radius[radius_check] \
                                                    and main_route[agent_checked][current_step][0] != main_route[agent_checked][0][0]\
                                                    and main_route[num_of_agent][current_step][0] != main_route[num_of_agent][0][0] \
                                                    and main_route[agent_checked][current_step][0] != main_route[agent_checked][len(main_route[agent_checked])-1][0] \
                                                    and main_route[num_of_agent][current_step][0] != main_route[num_of_agent][len(main_route[num_of_agent])-1][0]:
                                                print('NOT VALID', file, current_step, agent_checked, num_of_agent)





        path = '..'
        os.chdir(path)
    path = '..'
    os.chdir(path)

    print('All Routes are Valid')
    return True


###################################################################################
# INPUT UI
###################################################################################
global map_file_name
global data_folder
global MDR_factor

master = Tk()
Label(master, text="Room File").grid(row=0)
Label(master, text="Data Folder").grid(row=1)

e1 = Entry(master)
e2 = Entry(master)

e1.insert(10, config.var_a)
e2.insert(10, config.var_b)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

Button(master, text='Check Validation', command=check_route_validation).grid(row=7, column=1, sticky=W, pady=4)

mainloop()

map_file_name = e1.get()
data_folder = e2.get()



