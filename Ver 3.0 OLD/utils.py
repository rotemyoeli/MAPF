
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
            if (neighbor[0] > grid_tmp.shape[0] or neighbor[1] > grid_tmp.shape[1]) or grid_tmp[neighbor] == 1:
                continue
            else:
                grid_tmp[neighbor] = 1
                return grid_tmp, neighbor
        for i, j in neighbors:
            neighbor = (current_agent_pos[0] + i, current_agent_pos[1] + j)
            grid_tmp, neighbor = find_free_place(grid_tmp, neighbor, neighbors)
            return grid_tmp, neighbor


##############################################################################
# Return the radius - robust around the agent no. 0 - The adverarial
##############################################################################

def get_radius(array, current_agt_pos, robust_param, route, current_agent_no, Is_MDR):

    if Is_MDR == 0:
        current_agent_no = 0

    robust_radius = []
    if robust_param == 0:
        if current_agt_pos[1] < len(route[0])-1:
            robust_radius.append(route[current_agent_no][current_agt_pos[1]][0])

        return robust_radius

    if current_agt_pos[1] < len(route[0]) - 1:
        left_up = (route[0][current_agt_pos[1]][0][0] - (2 * robust_param), route[0][current_agt_pos[1]][0][1] - (2 * robust_param))
    else:
        return robust_radius

    if robust_param == 0:
        length = 0
    else:
        length = (robust_param * 4) + 1

    for step_right in range(0, length):
        for step_down in range(0, length):
            neighbor = (left_up[0] + step_right, left_up[1] + step_down)

            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:
                    if array[neighbor[0]][neighbor[1]] == 1:
                        # array bound 1 on map
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue

            robust_radius.append(neighbor)

    return robust_radius

##############################################################################
# Return the radius - robust around the agent no. 0 - The adversarial
##############################################################################

def get_valid_step(array, current_agt_pos, current_robust, route, current_agent_no):

    valid_radius = []
    robust_radius = []

    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0),
                 (1, 1), (1, -1), (-1, 1),
                 (-1, -1), (0, 0)]

    for i, j in neighbors:

        neighbor = (current_agt_pos[0][0] + i, current_agt_pos[0][1] + j)

        if 0 <= neighbor[0] < array.shape[0]:
            if 0 <= neighbor[1] < array.shape[1]:
                if array[neighbor[0]][neighbor[1]] == 1:
                    # array bound 1 on map
                    continue
            else:
                # array bound y walls
                continue
        else:
            # array bound x walls
            continue

        valid_radius.append(neighbor)
    # If this is the adversarial agent a0 then no need the radius just the valid steps
    if current_agent_no == 0:
        return valid_radius

    robust_radius = get_radius(array, current_agt_pos, current_robust, route, current_agent_no, 0)

    # Remove all steps that in the robust radius of the adversarial agent a0
    rob_tmp = robust_radius.copy()
    val_tmp = valid_radius.copy()
    for i in val_tmp: # no need for index. just walk each items in the array
        for j in rob_tmp:
            if i == j: # if there is a match, remove the match.
                valid_radius.remove(j)

    # Remove all steps that collide with prev. agents between Agent1 and current_agent_no
    list_of_position = []

    for agent_validation in range(0, current_agent_no):
        if (len(route[agent_validation]) - 1 > current_agt_pos[1]):
            list_of_position.append(route[agent_validation][current_agt_pos[1]][0])

    list_tmp = list(dict.fromkeys(list_of_position))
    val_tmp = valid_radius.copy()
    for i in val_tmp:  # no need for index. just walk each items in the array
        for j in list_tmp:
            if i == j:  # if there is a match, remove the match.
                valid_radius.remove(j)

    return valid_radius

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


def get_MDR_radius(array, neighbor, route, adversarial_agent, step, robust_factor):

    is_valid = False

    # Check if next step bound on wall
    if 0 <= neighbor[0][0] < array.shape[0]:
        if 0 <= neighbor[0][1] < array.shape[1]:
            if array[neighbor[0][0]][neighbor[0][1]] == 1:
                # array bound 1 on map
                return is_valid
        else:
            # array bound y walls
            return is_valid
    else:
        # array bound x walls
        return is_valid

    for check_robust in range(1, len(route)):
        # If agent is on its start position
        #if current_node.pos[check_robust] == route[check_robust][0][0]:
            #is_valid = True
         #   return is_valid

        if neighbor[1] >= len(route[check_robust]):
            current_step = len(route[check_robust]) - 1
        else:
            current_step = neighbor[1]

        robust_radius = get_radius(array, (route[check_robust][current_step]), robust_factor, route, check_robust, 1)

        if neighbor[0] in robust_radius:
            return is_valid

    is_valid = True
    return is_valid