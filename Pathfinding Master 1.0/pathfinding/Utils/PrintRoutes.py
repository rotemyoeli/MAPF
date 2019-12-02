# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 08:05:00 2018

@author: rotem
"""
#############################################################################
# import packages
##############################################################################
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import csv
import ast


def print_route(map_file, route_file):
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
