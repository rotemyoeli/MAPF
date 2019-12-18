#############################################################################
# import packages
##############################################################################
import random
import numpy as np
import os
from tkinter import *
import itertools as itert
from pathfinding.Utils import utils
import pandas as pd

from pathfinding.Core.diagonal_movement import DiagonalMovement
from pathfinding.Core.grid import Grid
from pathfinding.SearchAlgorithms.a_star import AStarFinder
###################################################################################
# Main Setup Route
###################################################################################
def create_routes(map_file_name, data_folder, robust_factor, num_of_agents, num_of_routes):
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
    for current_robust_factor in range(0, robust_factor+1):
        path = data_folder + "/" + "Robust_" + str(current_robust_factor)
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)

        ##################################################
        # Set here the number of unique routes
        ##################################################
        for current_route in range(0, num_of_routes):
            if current_route >= len(order_arr):
                break

            current_agents_order = order_arr[current_route]
            current_agents_order = list(map(int, current_agents_order))
            routes = [[] for i in range(num_of_agents)]

            for agent_no in range(0, num_of_agents):

                ############################
                # Reset the grid
                ############################
                grid1 = Grid(matrix=grid)
                start = grid1.node(starts_arr[current_agents_order[agent_no]][1], starts_arr[current_agents_order[agent_no]][0])
                goal = grid1.node(goals_arr[current_agents_order[agent_no]][1], goals_arr[current_agents_order[agent_no]][0])

                finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
                path, runs = finder.find_path(start, goal, grid1, routes, agent_no, current_robust_factor)
                # routes.append(path)
                routes[agent_no] = path
                print('operations:', runs, 'path length:', len(path))
                print(grid1.grid_str(path=path, start=start, end=goal))
                for x in range(0, len(routes)):
                    print(routes[x])

            ##################################################
            # Save routes to csv file
            ##################################################
            df_res = pd.DataFrame(routes)
            file_name_csv = "Route-" + str(current_route+1) + '_Agents-' + str(num_of_agents) + '_Robust-' + str(current_robust_factor) + '.csv'
            print(file_name_csv)
            df = pd.DataFrame(routes)
            df.to_csv(file_name_csv, index=False, header=False)

        path = '..'
        os.chdir(path)
    path = '..'
    os.chdir(path)