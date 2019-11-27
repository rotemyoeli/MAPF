
#############################################################################
# import packages
##############################################################################
import math
import random
import numpy as np
import heapq
import matplotlib.pyplot as plt
import pandas as pd
import os
from os.path import expanduser
import glob
import openpyxl as openpyxl
import csv
#import utils
from tkinter import filedialog
from tkinter import *
import config
import itertools as itert
#import ConverttoCSV
import utils


from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

###################################################################################
# Main Setup Route
###################################################################################
def main():
    map_file_name = e1.get()
    data_folder = e2.get()
    robust_factor = int(e4.get())
    num_of_agents = int(e5.get())

    # load the map file into numpy array
    with open(map_file_name, 'rt') as infile:
        grid1 = np.array([list(line.strip()) for line in infile.readlines()])
    print('Grid shape', grid1.shape)

    grid1[grid1 == '@'] = 0  # object on the map
    grid1[grid1 == 'T'] = 0  # object on the map
    grid1[grid1 == '.'] = 1  # free on map

    grid = np.array(grid1.astype(np.int))

    path = data_folder + '\\'
    os.chdir(path)

    starts_arr, goals_arr = utils.get_positions(grid, num_of_agents)

    for reset_grid in range(0, len(starts_arr)):
        grid[starts_arr[reset_grid]] = 1
        grid[goals_arr[reset_grid]] = 1

    #########################################
    # build unique agents order array
    #########################################
    tmp_str = ''
    for build_str in range(0, num_of_agents):
        tmp_str = tmp_str + str(build_str)
    order_arr = list(itert.permutations(tmp_str, num_of_agents))
    random.shuffle(order_arr)

    grid1 = Grid(matrix=grid)


    ##################################################
    # Create the no. of different Directories/robust
    ##################################################
    for current_robust_factor in range(2, 3):#robust_factor + 1):
        path = str(current_robust_factor) + '\\'
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)

        ##################################################
        # Set here the number of unique routes
        ##################################################
        for current_route in range(0, 1):#len(order_arr)):
            current_agents_order = order_arr[current_route]
            current_agents_order = list(map(int, current_agents_order))
            route = []
            for agent_no in range(0, num_of_agents):

                ############################
                # Reset the grid
                ############################
                grid1 = Grid(matrix=grid)
                start = grid1.node(starts_arr[current_agents_order[agent_no]][1], starts_arr[current_agents_order[agent_no]][0])
                goal = grid1.node(goals_arr[current_agents_order[agent_no]][1], goals_arr[current_agents_order[agent_no]][0])

                finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
                path, runs = finder.find_path(start, goal, grid1, route, agent_no, current_robust_factor)
                route.append(path)
                print('operations:', runs, 'path length:', len(path))
                print(grid1.grid_str(path=path, start=start, end=goal))
                for x in range(0, len(route)):
                    print(route[x])


###################################################################################
# INPUT UI
###################################################################################
global map_file_name
global data_folder
global robust_param
global min_num_of_agents
global max_num_of_SG
global is_random_SG
global selected_route

def show_entry_fields():
    print("Room File: %s\nData Folder: %s\nRobust Factor: %s\nNumber of Agents: %s\nMax Number of SG: %s\nNumber of Routes: %s" % (e1.get(), e2.get(), e4.get(), e5.get(), e6.get(), e7.get()))

def browse_button():
    filename = filedialog.askopenfilename()
    e1.insert(10, filename)
    return filename

def browse_file_button():
    filename = filedialog.askdirectory()
    e2.insert(10, filename)
    return filename

def browse_route_button():
    filename = filedialog.askdirectory()
    e9.insert(10, filename)
    return filename

def plot_route():

    PrintRoutes.print_route(e1.get(),e2.get(), e9.get())


master = Tk()
Label(master, text="Room File").grid(row=0)
Label(master, text="Data Folder").grid(row=2)
Label(master, text="Robust Factor").grid(row=4)
Label(master, text="Number of Agents").grid(row=6)


e1 = Entry(master)
e2 = Entry(master)
e4 = Entry(master)
e5 = Entry(master)
e8 = Entry(master)


e1.insert(10, config.var_a)
e2.insert(10, config.var_b)
e4.insert(10, config.var_d)
e5.insert(10, config.var_e)

e1.grid(row=0, column=1)
e2.grid(row=2, column=1)
e4.grid(row=4, column=1)
e5.grid(row=6, column=1)



data_folder = e2.get()
robust_param = e4.get()

Button(master, text='Run', command=main).grid(row=12, column=0, sticky=W, pady=4)
#Button(master, text='Convert Stp1', command=ConverttoCSV.step_one).grid(row=12, column=2, sticky=W, pady=4)
#Button(master, text='Convert Stp2', command=ConverttoCSV.step_two).grid(row=13, column=2, sticky=W, pady=4)
button2 = Button(text="Browse", command=browse_button).grid(row=0, column=2)
button3 = Button(text="Browse", command=browse_file_button).grid(row=2, column=2)

mainloop()