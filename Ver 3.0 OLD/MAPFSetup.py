# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 08:05:00 2018

@author: rotem
"""
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
import utils
from tkinter import filedialog
from tkinter import *
import config
import itertools as itert
import ConverttoCSV





def in_start_state(current, route, stp, y):
    is_in_start = False
    for check_start in range(0, stp):
        if route[y][check_start][0] == current[0]:
            is_in_start = True
        else:
            return False
    return is_in_start

def _compute_makespan(routes):
    return max([len(route) for route in routes])

##############################################################################
# heuristic function for heuristic_interrupt path scoring
##############################################################################
'''
search_node contains position of all agent, allowed abnormal moves, current time step
routes contains the planned routes for all agents [ including the path they passed so far ]
'''
def f_interrupt(self, search_node, routes):

    cost_without_interrupts = MDR._compute_makespan(routes)

    # An overestimate of the cost added by the abnormal moves
    remaining_abnormal_moves = search_node.k
    num_of_agents = len(search_node.pos)

    # The idea is that the maximal addition for each abnormal move is that it will delay all agents by one time step.
    return -1*(cost_without_interrupts + num_of_agents * remaining_abnormal_moves)  # TODO: CHANGE 2

    '''
     route = list containing the planned route for each agent 
    '''

def is_goal(self, node, route):

    for x in range(0, len(node.pos)):
        if node.pos[x] is not route[x][-1][0] and node.pos[x] is not None:
            return False
    return True

##############################################################################
# heuristic function for path scoring
##############################################################################

def heuristic(a, b):
    distance = (abs(b[0] - a[0]) + abs(b[1] - a[1]))
    return distance


##############################################################################
# get start and goal for all agents (not the lead)
##############################################################################

def get_positions(grid_tmp, agent_number):
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    new_starts = []
    new_goals = []
    x_size = grid_tmp.shape[0]
    y_size = grid_tmp.shape[1]

    # set the first agent S&G positions on valid places on the grid
    start_is_set = 0
    goal_is_set = 0
    while start_is_set == 0:

        new_starts.append((random.sample(range(0, x_size), 1)[0], random.sample(range(0, y_size), 1)[0]))

        if grid_tmp[new_starts[0]] == 1:
            new_starts = []
            continue
        else:
            grid_tmp[new_starts[0]] = 1
            start_is_set = 1
            break
    while goal_is_set == 0:

        new_goals.append((random.sample(range(0, x_size), 1)[0], random.sample(range(0, y_size), 1)[0]))

        if grid_tmp[new_goals[0]] == 1:
            new_goals = []
            continue
        else:
            grid_tmp[new_goals[0]] = 1
            goal_is_set = 1
            break


    # set all S&G according the leader
    for num_of_SG in range(1, agent_number):
        # Find start position for the next agent
        current_agent_pos = new_starts[0]
        grid_tmp, neighbor = utils.find_free_place(grid_tmp, current_agent_pos, neighbors)
        new_starts.append(neighbor)

        # Find goal position for the next agent
        current_agent_pos = new_goals[0]
        grid_tmp, neighbor = utils.find_free_place(grid_tmp, current_agent_pos, neighbors)
        new_goals.append(neighbor)

    ########################################
    # Fixed routes for testing
    ########################################
    #new_starts = [(10, 5), (11, 5), (12, 5), (10, 4), (11, 5)]
    #new_goals = [(12, 10), (10, 10), (11, 10), (11, 11), (12, 11)]

    return new_starts, new_goals


def astar(array, start, goal, current_agent_no, route, robust_dist):
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1), (0, 0)]

    start_node = (start, 0)
    close_set = set()
    came_from = {start_node: 0}
    gscore = {start_node: 0}
    fscore = {start_node: heuristic(start, goal)}
    oheap = []
    heapq.heappush(oheap, (fscore[start_node], start_node))
    is_collision = 0
    data = []

    while oheap:
        current = heapq.heappop(oheap)[1]
        if current[0] == goal:
            while current in came_from:
                data.append((current[0], current[1]))
                current = came_from[current]
            data = list(reversed(data))
            return data

        close_set.add(current)

        action_cost = 1  # TODO: Replace this in the future to support different action costs

        for op in neighbors:
            (i, j) = op
            neighbor = ((current[0][0] + i, current[0][1] + j), current[1] + action_cost)
            neighbor_is_valid = 0
            tentative_g_score = gscore[current] + action_cost

            # Get valid steps (radius)
            valid_radius = utils.get_valid_step(array, neighbor, robust_dist, route, current_agent_no)

            if len(valid_radius) == 0:
                neighbor = ((current[0][0], current[0][1]), current[1] + action_cost)
                neighbor_is_valid = 1

            neighbor_tmp = neighbor[0]
            val_tmp = valid_radius.copy()
            for i in val_tmp:

                # Check 180 deg. to goal

                current_radians = math.atan2(goal[1] - current[0][1],
                                             goal[0] - current[0][0])
                current_degrees = math.degrees(current_radians)

                next_step_radians = math.atan2(i[1] - current[0][1],
                                               i[0] - current[0][0])
                next_step_degrees = math.degrees(next_step_radians)

                anglediff = (next_step_degrees - current_degrees + 180 + 360) % 360 - 180

                if i == neighbor_tmp:
                    if (anglediff > 90 or anglediff < -90):
                        neighbor_is_valid = 0
                    else:
                        neighbor_is_valid = 1

            if neighbor_is_valid == 0:
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor[0], 0):
                continue

            if tentative_g_score < gscore.get(neighbor[0], 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = (current)
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor[0], goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))


    return data






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

    grid1[grid1 == '@'] = 1  # object on the map
    grid1[grid1 == 'T'] = 1  # object on the map
    grid1[grid1 == '.'] = 0  # free on map

    grid = np.array(grid1.astype(np.int))
    path = data_folder + '\\'
    os.chdir(path)

    starts_arr, goals_arr = get_positions(grid, num_of_agents)

    for reset_grid in range(0, len(starts_arr)):
        grid[starts_arr[reset_grid]] = 0
        grid[goals_arr[reset_grid]] = 0

    #########################################
    # build unique agents order array
    #########################################
    tmp_str = ''
    for build_str in range(0, num_of_agents):
        tmp_str = tmp_str + str(build_str)
    order_arr = list(itert.permutations(tmp_str, num_of_agents))
    random.shuffle(order_arr)

    ####################################
    # Create the no. of different routes
    ####################################
    for current_robust_factor in range(0, robust_factor + 1):

        path = str(current_robust_factor) + '\\'

        if not os.path.exists(path):
            os.makedirs(path)

        os.chdir(path)


    # Set here the number of unique routes
        for current_route in range(0, len(order_arr)):

            current_agent = order_arr[current_route]
            current_agent = list(map(int, current_agent))
            route = []

            for x in range(0, num_of_agents):

                start = (starts_arr[current_agent[x]][0], starts_arr[current_agent[x]][1])
                goal = (goals_arr[current_agent[x]][0], goals_arr[current_agent[x]][1])


                ##############################################################################
                # Calling A*
                ##############################################################################

                route.append(astar(grid, start, goal, x, route, current_robust_factor))

                if route:
                    print('-' * 20, 'Agent No. - ', x, '-' * 20)
                    print('Start point - ', start, '\nGoal point  - ', goal)
                    print('Len of the route - ', len(route[x]))
                    print('-' * 56, '\n')

            # Write to Excel
            df_res = pd.DataFrame(route)

            file_name = []
            file_name.append('Res')
            file_name.append(str(num_of_agents))
            file_name.append('_Agents')
            file_name.append(str(current_route))
            file_name.append('_RouteNo')
            file_name.append(str(current_robust_factor))
            file_name.append('_Robust_index')
            file_name.append('.xlsx')
            file_n = ' '.join(file_name)
            file_n.replace(" ", "")

            print(file_n)

            writer_xl = pd.ExcelWriter(file_n, engine='openpyxl')
            df_res.to_excel(writer_xl, sheet_name='Agents', index=False)
            writer_xl.save()
            writer_xl.close()
        path = '..'
        os.chdir(path)
    path = '..'
    os.chdir(path)
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
Button(master, text='Convert Stp1', command=ConverttoCSV.step_one).grid(row=12, column=2, sticky=W, pady=4)
Button(master, text='Convert Stp2', command=ConverttoCSV.step_two).grid(row=13, column=2, sticky=W, pady=4)
button2 = Button(text="Browse", command=browse_button).grid(row=0, column=2)
button3 = Button(text="Browse", command=browse_file_button).grid(row=2, column=2)

mainloop()




