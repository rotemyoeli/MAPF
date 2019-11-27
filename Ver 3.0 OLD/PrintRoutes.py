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
import pylab as pl
import pandas as pd
import os
import glob
import csv
import ast
from tkinter import filedialog
from tkinter import *
import config
import itertools as itert
import ConverttoCSV


def print_route(map_file, dir_name, route_file):
    route = []

    # load the map file into numpy array
    with open(map_file, 'rt') as infile:
        grid1 = np.array([list(line.strip()) for line in infile.readlines()])
    print('Grid shape', grid1.shape)

    grid1[grid1 == '@'] = 1 #object on the map
    grid1[grid1 == 'T'] = 1 #object on the map
    grid1[grid1 == '.'] = 0 #free on map

    grid = np.array(grid1.astype(np.int))

    # Plot the map
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(grid, cmap=plt.cm.gray)

    counter = 0
    route = []

    path = route_file
    extension = 'csv'
    os.chdir(path)
    files = [i for i in glob.glob('*.{}'.format(extension))]

    for file in files:
        if counter == 0:
            # reading csv file
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
                    route.append(tmp_route)
            counter = counter + 1



    ##############################################################################
    # plot the path
    ##############################################################################

    for x in range(0, len(route)):

        start = (route[x][0][0])
        goal = (route[x][-1][0])

        # extract x and y coordinates from route list
        x_coords = []
        y_coords = []

        if route:
            for i in (range(0, len(route[x]))):
                x1 = route[x][i][0][0]
                y1 = route[x][i][0][1]


                x_coords.append(x1)
                y_coords.append(y1)

        # plot path
        ax.scatter(start[1], start[0], marker="^", color="white", s=50)
        ax.scatter(goal[1], goal[0], marker="*", color="white", s=50)
        ax.plot(y_coords, x_coords, color="white")


    plt.grid(True)
    plt.show()

def main():

    map_file_name = e1.get()
    route_file_name = e9.get()
    # load the map file into numpy array
    with open(map_file_name, 'rt') as infile:
        grid1 = np.array([list(line.strip()) for line in infile.readlines()])
    print('Grid shape', grid1.shape)

    grid1[grid1 == '@'] = 1  # object on the map
    grid1[grid1 == 'T'] = 1  # object on the map
    grid1[grid1 == '.'] = 0  # free on map

    grid = np.array(grid1.astype(np.int))

    # Plot the map
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(grid, cmap=plt.cm.gist_gray)

    counter = 0
    route = []

    with open(route_file_name, 'rt') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        header = next(csvreader)
        # extracting each data row one by one
        for row in csvreader:
            tmp_route = []
            for y in range(0, len(row)):
                if row[y]:
                    tmp_route.append(ast.literal_eval(row[y]))
            route.append(tmp_route)
    counter = counter + 1

    ##############################################################################
    # plot the route
    ##############################################################################

    for x in range(0, len(route)):

        start = (route[x][0][0])
        goal = (route[x][-1][0])

        # extract x and y coordinates from route list
        x_coords = []
        y_coords = []

        if route:
            for i in (range(0, len(route[x]))):
                x1 = route[x][i][0][0]
                y1 = route[x][i][0][1]

                x_coords.append(x1)
                y_coords.append(y1)

        # plot path
        ax.scatter(start[1], start[0], marker="^", color="white", s=50)
        ax.scatter(goal[1], goal[0], marker="*", color="white", s=50)

        set_color_cycle = ['white', 'green', 'blue', 'yellow', 'red', 'cyan', 'magenta', 'purple', 'brown', 'pink', 'gray', 'olive']

        ax.plot(y_coords, x_coords, "-0", color=set_color_cycle[x])
        step_number = 0
        for x_1, y_1 in zip(y_coords, x_coords):
            pl.text(x_1, y_1, str(step_number), color=set_color_cycle[x], fontsize=11)
            step_number = step_number + 1
        pl.margins(0.1)

    plt.grid(True)
    plt.show()
###################################################################################
# INPUT UI
###################################################################################
global map_file_name
global selected_route
global show_numbers

def browse_button():
    filename = filedialog.askopenfilename()
    e1.insert(10, filename)
    return filename

def browse_file_button():
    filename = filedialog.askopenfilename()
    e9.insert(10, filename)
    return filename

def plot_route():
    PrintRoutes.print_route(e1.get(), e9.get())


master = Tk()
Label(master, text="Room File").grid(row=0)
Label(master, text="Select Route").grid(row=2)

e1 = Entry(master)
e9 = Entry(master)

e1.insert(10, config.var_a)

e1.grid(row=0, column=1)
e9.grid(row=2, column=1)

button2 = Button(text="Browse", command=browse_button).grid(row=0, column=2)
button4 = Button(text="Browse", command=browse_file_button).grid(row=2, column=2)
Button(master, text='Print Selected Route', command=main).grid(row=5, column=2, sticky=W, pady=4)


var1 = IntVar()
cb1 = Checkbutton(master, text="Include step no.", variable=var1).grid(row=3, column=1)

var1 = IntVar()

mainloop()
