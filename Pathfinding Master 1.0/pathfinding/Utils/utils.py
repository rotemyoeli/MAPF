
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
'''
Check if pos is a legal position in the map
'''
def is_legal(grid, pos):
    if 0 <= pos[0] < grid.shape[0]:
        if 0 <= pos[1] < grid.shape[1]:
            if grid[pos[0]][pos[1]] == 1:
                return False # array bound 1 on map
        else:
            return False # array bound y walls
    else:
        return False # array bound x walls
    return True

'''
Return a dictionary that maps every location to the distance from the given start
'''
def dijkstra(grid, source, operators):
    dist_to_source = dict()
    dist_to_source[source]=0

    oheap = []
    closed = set()
    heapq.heappush(oheap, (0, source))

    while oheap:
        (g, pos) = heapq.heappop(oheap)
        closed.add(pos)

        for i, j, cost in operators:
            neighbor = (pos[0] + i, pos[1] + j)
            new_g = g+cost

            if is_legal(grid, neighbor)==False:
                continue

            if neighbor in closed:
                continue

            if neighbor in dist_to_source:
                # If existing path is better
                if dist_to_source[neighbor]<=new_g:
                    continue
                # TODO: In the future,

            dist_to_source[neighbor]=new_g
            heapq.heappush(oheap,(new_g, neighbor))
    return dist_to_source



def find_free_place(grid_tmp, current_agent_pos, neighbors):

    current_not_set = 1
    while current_not_set == 1:
        for i, j in neighbors:
            neighbor = (current_agent_pos[0] + i, current_agent_pos[1] + j)
            if (neighbor[0] > grid_tmp.shape[0] or neighbor[1] > grid_tmp.shape[1]) or grid_tmp[neighbor] == 0:
                continue
            else:
                grid_tmp[neighbor] = 0
                return grid_tmp, neighbor
        for i, j in neighbors:
            neighbor = (current_agent_pos[0] + i, current_agent_pos[1] + j)
            grid_tmp, neighbor = find_free_place(grid_tmp, neighbor, neighbors)
            return grid_tmp, neighbor



##############################################################################
# Valid start according to the robust level
##############################################################################
def get_start_approval(array, start_pos, agent_no, route, robust_dist):

    radius = get_radius(array, start_pos[0], robust_dist)
    ##Check for collision
    for a in range(0, agent_no):

        for robust_check in range(0, robust_dist):

            if len(route[a]) > start_pos[1]:

                for radius_check in range(0, len(radius)):
                    if route[a][start_pos[1]][0] == radius[radius_check] and a != agent_no:
                        print('a -', a, 'agent no -', agent_no, route[a][start_pos[1]], radius[radius_check])

                        return False

    return True


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

        if grid_tmp[new_starts[0]] == 0:
            new_starts = []
            continue
        else:
            grid_tmp[new_starts[0]] = 0
            start_is_set = 1
            break
    while goal_is_set == 0:

        new_goals.append((random.sample(range(0, x_size), 1)[0], random.sample(range(0, y_size), 1)[0]))

        if grid_tmp[new_goals[0]] == 0:
            new_goals = []
            continue
        else:
            grid_tmp[new_goals[0]] = 0
            goal_is_set = 1
            break


    # set all S&G according the leader
    for num_of_SG in range(1, agent_number):
        # Find start position for the next agent
        current_agent_pos = new_starts[0]
        grid_tmp, neighbor = find_free_place(grid_tmp, current_agent_pos, neighbors)
        new_starts.append(neighbor)

        # Find goal position for the next agent
        current_agent_pos = new_goals[0]
        grid_tmp, neighbor = find_free_place(grid_tmp, current_agent_pos, neighbors)
        new_goals.append(neighbor)

    ########################################
    # Fixed routes for testing
    ########################################
    #new_starts = [(10, 5), (11, 5), (12, 5), (10, 4), (11, 5)]
    #new_goals = [(12, 10), (10, 10), (11, 10), (11, 11), (12, 11)]

    return new_starts, new_goals

##############################################################################
# Return the radius - robust around the agent no. 0 - The adverarial
##############################################################################

def get_radius(grid, node, robust_param, route, current_agent_no, Is_MDR):

    robust_radius = []

    if Is_MDR == 0:
        current_agent_no = 0
    if len(route) == 0:
        return robust_radius

    if robust_param == 0:
        if node.step < len(route[0])-1:
            robust_radius.append(route[current_agent_no][node.step])
        return robust_radius

    if node.step < len(route[0]) - 1:
        left_up = (route[0][node.step][0] - (2 * robust_param), route[0][node.step][1] - (2 * robust_param))
    else:
        return robust_radius

    if robust_param == 0:
        length = 0
    else:
        length = (robust_param * 4) + 1

    for step_right in range(0, length):
        for step_down in range(0, length):
            neighbor = (left_up[0] + step_right, left_up[1] + step_down)
            if grid.nodes[neighbor[0]][neighbor[1]].walkable:
                robust_radius.append(neighbor)
            else:
                continue
    return robust_radius