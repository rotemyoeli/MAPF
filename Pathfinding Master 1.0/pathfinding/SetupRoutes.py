
#############################################################################
# import packages
##############################################################################
import random
import numpy as np
import os
#import utils
from tkinter import *
import itertools as itert
from pathfinding.Utils import utils

from pathfinding.Core.diagonal_movement import DiagonalMovement
from pathfinding.Core.grid import Grid
from pathfinding.SearchAlgorithms.a_star import AStarFinder

global map_file_name
global data_folder
global robust_param
global min_num_of_agents
global max_num_of_SG
global is_random_SG
global selected_route
###################################################################################
# Main Setup Route
###################################################################################
def create_routes(map_file_name, data_folder, robust_factor, num_of_agents):
    # load the map file into numpy array
    with open(map_file_name, 'rt') as infile:
        grid1 = np.array([list(line.strip()) for line in infile.readlines()])
    print('Grid shape', grid1.shape)

    grid1[grid1 == '@'] = 0  # object on the map
    grid1[grid1 == 'T'] = 0  # object on the map
    grid1[grid1 == '.'] = 1  # free on map

    grid = np.array(grid1.astype(np.int))

    os.chdir(data_folder)

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
    for current_robust_factor in range(0, robust_factor):#robust_factor + 1):
        path = data_folder + "/" + "Robust_" + str(current_robust_factor)
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)

        ##################################################
        # Set here the number of unique routes
        ##################################################
        for current_route in range(0, 2):#len(order_arr)):
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

