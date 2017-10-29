import re
from pprint import pprint
import time
import math
import Queue as q_module

#####################################################################
############################SETUP START##############################
#####################################################################

def loadenv(filename):
    grid = []
    with open(filename) as f:
        for line in f.read().splitlines():
            char_l = list(line)
            grid.append(char_l)
    return grid

def refresh_env(env):
    time.sleep(0.1)
    print("\n")
    for l in env:
        print(l)
    print("\n")

def refresh_env_mod(env, v_orientation_d):
    time.sleep(0.1)
    mod_env = [x[:] for x in env]

    print("\n")
    for r, l in enumerate(mod_env):
        for c, s in enumerate(l):
            if len(v_orientation_d[(r,c)]) == 1:
                mod_env[r][c] = mod_env[r][c] + v_orientation_d[(r, c)][0]
            if len(mod_env[r][c]) == 1:
                mod_env[r][c] = mod_env[r][c] + "  "

    for l in mod_env:
        print(l)
    print("\n")

def get_colors(env):
    colors = set()
    for r, line in enumerate(env):
        for c, ch in enumerate(line):
            if ch != '_':
                colors.add(ch)
    return colors

def get_color_source_coords(env):
    color_source_coords = {}
    for r, line in enumerate(env):
        for c, ch in enumerate(line):
            if ch != '_':
                if ch in color_source_coords:
                    color_source_coords[ch].append((r, c))
                else:
                    color_source_coords[ch] = [(r, c)]
    return color_source_coords

def get_source_coords(env):
    source_coords = []
    for r, line in enumerate(env):
        for c, ch in enumerate(line):
            if ch != '_':
                source_coords.append((r, c))
    return source_coords

env = loadenv('input10102.txt')
inputs = ["input55.txt", "input77.txt", "input88.txt",
"input991.txt", "input10101.txt", "input10102.txt",
"input1212.txt", "input1214.txt", "input1414.txt"]
refresh_env(env)
color_source_mapping = get_color_source_coords(env)
print(color_source_mapping)
colors = get_colors(env)
print(colors)
source_coords = get_source_coords(env)
print(source_coords)


def manhattan_dist(coord1, coord2):
    i1, j1 = coord1
    i2, j2 = coord2
    return abs(j2-j1) + abs(i2-i1)

def distance_to_source(coord, source_coords):
    min_dist = 9999999
    for source_coord in source_coords:
        dist = manhattan_dist(coord, source_coord)
        if dist < min_dist:
            min_dist = dist
    return min_dist

def get_variable_domains(env):
    variable_orientation_domains = {}
    variable_color_domains = {}
    for r, line in enumerate(env):
        for c, ch in enumerate(line):
            if ch == '_':
                variable_orientation_domains[(r, c)] = ['NE', 'SE', 'SW', 'NW', 'VE', 'HO']
                variable_color_domains[(r,c)] = list(get_colors(env))
            else:
                variable_orientation_domains[(r, c)] = ['SO']
                variable_color_domains[(r, c)] = [ch]
    return variable_orientation_domains, variable_color_domains


v_orientation_d, v_color_d = get_variable_domains(env)

print(v_orientation_d)
print(v_color_d)

print("############SETUP COMPLETE############")
########################################################################
############################SETUP COMPLETE##############################
########################################################################


def has_open_end_facing_curr(curr, other, other_pipe_type):
    this_i, this_j = curr
    other_i, other_j = other

    delta_i = this_i - other_i
    delta_j = this_j - other_j

    if delta_i == 1:
        if other_pipe_type == "SE" or \
            other_pipe_type == "SW" or \
            other_pipe_type == "VE":
            return True

    elif delta_i == -1:
        if other_pipe_type == "NE" or \
            other_pipe_type == "NW" or \
            other_pipe_type == "VE":
            return True

    if delta_j == 1:
        if other_pipe_type == "NE" or \
            other_pipe_type == "SE" or \
            other_pipe_type == "HO":
            return True
    elif delta_j == -1:
        if other_pipe_type == "NW" or \
            other_pipe_type == "SW" or \
            other_pipe_type == "HO":
            return True

    return False








def check_constraints(curr_coord, env, pipe_type, curr_color, v_orientation_d, v_color_d):
    """
    return True if pipe type and color satisfies constraints (consistent) for this variable, curr_coord
    return False otherwise
    """
    i, j = curr_coord


    #for neighbors that aren't empty or sources
    	#if it has an open end facing us
    	#then it must have the same color as us
    	#and we must have an open end facing it
    cardinal_dirs = [(i-1, j), (i, j+1), (i+1, j), (i, j-1)]
    cardinal_dirs = [cd for cd in cardinal_dirs if is_coord_in_bounds((cd[0], cd[1]), env)]
    cardinal_dirs = [cd for cd in cardinal_dirs if env[cd[0]][cd[1]] != '_']
    cardinal_dirs = [cd for cd in cardinal_dirs if v_orientation_d[cd][0] != 'SO']
    cardinal_dirs = [cd for cd in cardinal_dirs if has_open_end_facing_curr(curr_coord, cd, v_orientation_d[cd][0])]
    for cd in cardinal_dirs:
        cd_i, cd_j = cd
        other_pipe_color = env[cd_i][cd_j]
        if not pipe_has_open_end_facing_other(curr_coord, cd, pipe_type):
            return False
        if other_pipe_color != curr_color:
            return False


    #for neighbors that aren't empty or sources or out of bounds and **are at our open ends**
        #they must be the same color as current
        #they must have open end facing current
    open_end_coords = get_open_end_coords(curr_coord, pipe_type)
    for oec in open_end_coords:
        if not is_coord_in_bounds(oec, env):
            return False
    open_end_coords = [oec for oec in open_end_coords if env[oec[0]][oec[1]] != '_']
    open_end_coords = [oec for oec in open_end_coords if v_orientation_d[oec][0] != 'SO']
    for open_end_coord in open_end_coords:
        next_i, next_j = open_end_coord
        open_end_coord_color = env[next_i][next_j]

        if open_end_coord_color != curr_color and open_end_coord_color != '_': #purposely rechecking color for posterity
            return False

        if not has_open_end_facing_curr(curr_coord, \
            open_end_coord, \
            v_orientation_d[open_end_coord][0]):
            return False



    #for neighbors that are sources and **are at our open ends**
        #they must be the same color as current
        #they must not have any other neighbors with our color
    open_end_coords = get_open_end_coords(curr_coord, pipe_type)
    open_end_coords = [oec for oec in open_end_coords if env[oec[0]][oec[1]] != '_']
    open_end_coords = [oec for oec in open_end_coords if v_orientation_d[oec][0] == 'SO']
    for open_end_coord in open_end_coords:
        next_i, next_j = open_end_coord
        open_end_coord_color = env[next_i][next_j]

        if open_end_coord_color != curr_color and open_end_coord_color != '_': #purposely rechecking color for posterity
            return False

        if v_orientation_d[open_end_coord][0] == 'SO':
            source_dirs = [(next_i-1, next_j), (next_i, next_j+1), (next_i+1, next_j), (next_i, next_j-1)]
            #let's get rid of cd's that are out of bounds
            source_dirs = [sd for sd in source_dirs if is_coord_in_bounds((sd[0], sd[1]), env)]
            source_dirs_with_same_color = [sd for sd in source_dirs if env[sd[0]][sd[1]] == curr_color]
            if len(source_dirs_with_same_color) >= 1:
                return False


    #check for zig zags by considering the squares made with
        #(i, j) in the center
        #ensure that each square does not share the same color 4 times
    NE_cluster = [(i-1, j), (i-1, j+1), (i, j+1)] #imagine (i, j) is included
    SE_cluster = [(i, j+1), (i+1, j+1), (i+1, j)] #imagine (i, j) is included
    SW_cluster = [(i+1, j), (i+1, j-1), (i, j-1)] #imagine (i, j) is included
    NW_cluster = [(i, j-1), (i-1, j-1), (i-1, j)] #imagine (i, j) is included
    clusters = [NE_cluster, SE_cluster, SW_cluster, NW_cluster]

    for cluster in clusters:
        color_cnt = 1 #(i, j) was included, let's use (i, j) color
        for cluster_coord in cluster:
            r, c = cluster_coord
            if is_coord_in_bounds(cluster_coord, env) and env[r][c] == curr_color:
                color_cnt += 1
        if color_cnt == 4:
            return False #zig zag detected



    return True




























def get_open_end_coords(coord, pipe_type):
    open_end_coords = []
    i, j = coord
    if pipe_type == 'NE':
        open_end_coords = [(i-1, j), (i, j+1)]
    elif pipe_type == 'SE':
        open_end_coords = [(i+1, j), (i, j+1)]
    elif pipe_type == 'SW':
        open_end_coords = [(i+1, j), (i, j-1)]
    elif pipe_type == 'NW':
        open_end_coords = [(i-1, j), (i, j-1)]
    elif pipe_type == 'VE':
        open_end_coords = [(i+1, j), (i-1, j)]
    elif pipe_type == 'HO':
        open_end_coords = [(i, j+1), (i, j-1)]
    elif pipe_type == 'SO':
        open_end_coords = [(i-1, j), (i, j+1), (i+1, j), (i, j-1)]
    return open_end_coords

def pipe_has_open_end_facing_other(pipe_coord, other_coord, curr_pipe_type):
    curr_open_end_coords = get_open_end_coords(pipe_coord, curr_pipe_type)
    return other_coord in curr_open_end_coords

def is_coord_in_bounds(coord, env):
    r, c = coord
    return r >= 0 and r < len(env) and c >= 0 and c < len(env[0])

def is_assignment_complete(env, v_orientation_d, v_color_d):
    for r, line in enumerate(env):
        for c, ch in enumerate(line):
            if ch == '_':
                return False
    return True

def select_most_constrained_variable(env, v_orientation_d, v_color_d):
    min_var_vals = 99999
    min_var = (-1, -1)
    for r, line in enumerate(env):
        for c, ch in enumerate(line):
            if ch == '_':
                var_val_cnt = count_variable_values((r, c), env, v_orientation_d, v_color_d)
                if var_val_cnt < min_var_vals:
                    min_var = (r, c)
                    min_var_vals = var_val_cnt
    return min_var



from random import shuffle
shuffled_coords = []
for r, line in enumerate(env):
    for c, ch in enumerate(line):
        if ch == '_':
            shuffled_coords.append((r, c))
shuffle(shuffled_coords)

def select_unassigned_variable_random(env):
    for coord in shuffled_coords:
        if env[coord[0]][coord[1]] == '_':
            return coord



def select_unassigned_variable_dumb(env):
    for r, line in enumerate(env):
        for c, ch in enumerate(line):
            if ch == '_':
                return (r, c)






def count_variable_values(variable_coordinate, env, v_orientation_d, v_color_d):
    """
    for this variable (location) count how many values are consistent in its domain.
    useful for least constraining value heuristic
    useful for most constrained variable heuristic
    """
    i, j = variable_coordinate
    v_o = v_orientation_d[(i, j)]
    v_c = v_color_d[(i, j)]
    if env[i][j] == '_':
        return len(v_o) * len(v_c)
    elif v_o == 'SO':
        return 0
    else:
        val_cnt = 0
        for o in v_o:
            for c in v_c:
                if check_constraints((i, j), env, o, c, v_orientation_d, v_color_d):
                    val_cnt += 1
        return val_cnt

def select_least_constraining_values(variable_coordinate, env, v_orientation_d, v_color_d):
    v_orientations = v_orientation_d[variable_coordinate]
    v_colors = v_color_d[variable_coordinate]

    values = []


    for v_orientation in v_orientations:
        for v_color in v_colors:
            #assign this value
            i, j = variable_coordinate
            #TEMPORARY STORAGE
            temp_color = env[i][j]
            temp_orientation_domain = v_orientation_d[variable_coordinate]
            temp_color_domain = v_color_d[variable_coordinate]

            #assign the variable
            env[i][j] = v_color
            v_orientation_d[variable_coordinate] = [v_orientation]
            v_color_d[variable_coordinate] = [v_color]

            val_sum = 0
            cardinal_dirs = [(i-1, j), (i, j+1), (i+1, j), (i, j-1)]
            cardinal_dirs = [cd for cd in cardinal_dirs if is_coord_in_bounds((cd[0], cd[1]), env)]

            for cd in cardinal_dirs:
                val_sum += count_variable_values(cd, env, v_orientation_d, v_color_d)



            #REASSIGN WITH TEMPORARY VALUES
            env[i][j] = temp_color
            v_orientation_d[variable_coordinate] = temp_orientation_domain
            v_color_d[variable_coordinate] = temp_color_domain

            values.append((val_sum, v_orientation, v_color))

    values.sort()
    values = [(v[1], v[2]) for v in values]
    return reversed(values)
    # return values


import itertools
def select_values_dumb(variable_coordinate, env, v_orientation_d, v_color_d):
    v_orientations = v_orientation_d[variable_coordinate]
    v_colors = v_color_d[variable_coordinate]
    return list(itertools.product(v_orientations, v_colors))


def get_actions(r, c):
    return [(r-1, c), (r, c+1), (r+1, c),(r, c-1)]

def get_valid_actions(curr_node, maze_map, color):
    r, c = curr_node
    actions = get_actions(r, c)
    return [action_coord for action_coord in actions if is_valid_action(action_coord, maze_map, color)]

#helper method to get_valid_actions
def is_valid_action(action_coord, maze_map, color):
    r, c = action_coord
    if r >= 0 and r < len(maze_map) and c >= 0 and c < len(maze_map[0]) and (maze_map[r][c] == "_" or maze_map[r][c] == color):
        return True
    return False

def bfs(source, target, env, color):
    q = []
    visited = set()
    q.append(source)
    while len(q) != 0:
        curr = q.pop(0)
        if curr in visited:
            continue
        if curr == target:
            return True

        visited.add(curr)
        valid_actions = get_valid_actions(curr, env, color)
        valid_actions = [a for a in valid_actions if a not in visited]

        for a in valid_actions:
            q.append(a)
    return False


def can_reach_sources(env, v_orientation_d, v_color_d):
    flag = True
    for color in color_source_mapping:
        csm = color_source_mapping[color]
        s1 = csm[0]
        s2 = csm[1]
        if not bfs(s1, s2, env, color):
            flag = False

    return flag

#v_orientation_d: variable_orientation_domains maps location to domain ['NE', 'SE', 'SW', 'NW', 'VE', 'HO'] or ['SO']
#v_color_d: variable_color_domains maps location to the domain of colors given
#env: environment (the grid)
global_cnt = [0]
import copy
import sys
import random
def backtrack(env, v_orientation_d, v_color_d):
    global_cnt[0] = global_cnt[0] + 1
    # if global_cnt[0] > 10:
    #     sys.exit()

    # if global_cnt[0] % 10000 == 0: #991 is a prime number
    #     refresh_env_mod(env, v_orientation_d)
    # refresh_env_mod(env, v_orientation_d)
    if is_assignment_complete(env, v_orientation_d, v_color_d):
        return env

    #TODO the below line of code may cause a infinite loop
    variable_coordinate = select_most_constrained_variable(env, v_orientation_d, v_color_d)

    values = select_least_constraining_values(variable_coordinate, env, v_orientation_d, v_color_d)
    # values = select_values_dumb(variable_coordinate, env, v_orientation_d, v_color_d)
    for v_orientation, v_color in values:
        if check_constraints(variable_coordinate, env, v_orientation, v_color, v_orientation_d, v_color_d):
            i, j = variable_coordinate
            #TEMPORARY STORAGE
            temp_color = env[i][j]
            temp_orientation_domain = v_orientation_d[variable_coordinate]
            temp_color_domain = v_color_d[variable_coordinate]

            #assign the variable
            env[i][j] = v_color
            v_orientation_d[variable_coordinate] = [v_orientation]
            v_color_d[variable_coordinate] = [v_color]

            result = None
            #backtrack
            flag = True
            # if random.random() > 0.1:
            # flag = can_reach_sources(env, v_orientation_d, v_color_d)

            if flag:
                result = backtrack(env, v_orientation_d, v_color_d)

            if result == None:
                #REASSIGN WITH TEMPORARY VALUES
                env[i][j] = temp_color

                v_orientation_d[variable_coordinate] = temp_orientation_domain
                v_color_d[variable_coordinate] = temp_color_domain

            else:
                #CORRECT SOLUTION
                return result
    return None
from datetime import datetime
startTime = datetime.now()
refresh_env(env)
backtrack_result = backtrack(env, v_orientation_d, v_color_d)

if backtrack_result == None:
    print("backtracking failed")
else:
    print("final result: ")
    print("variable assignments made: ", global_cnt[0])
    print("time")
    print datetime.now() - startTime
    print()
    refresh_env_mod(env, v_orientation_d)
    refresh_env(env)
