from __future__ import print_function
from search_enums import *
from Queue import PriorityQueue

import copy
import math
import numpy as np

INITIAL_POSITION_INDICATOR = 'P'
FOOD_PELLET = '.'
SELECTED_PATH = '.'
PATH = ' '
WALL = '%'

def find_all_occurrences(pattern, text):
    i = text.find(pattern)
    while i != -1:
        yield i
        i = text.find(pattern, i + 1)

distances_memory = {}
msts_memory = {}

class PacmanProblemState:
    def __init__(self, position, food_positions = set()):
        self.position = position
        self.food_positions = food_positions
        self.has_food = position in food_positions
        # for discarding from the frontier if a better one is evaluated.
        self.priority = 0

    def __eq__(self, item):
        return self.position == item.position and \
                self.has_food == item.has_food and \
                self.food_positions == item.food_positions

    def __ne__(self, item):
        return self.position != item.position or \
                self.has_food != item.has_food or \
                self.food_positions != item.food_positions

    def __cmp__(self, item):
        if self.has_food and not item.has_food:
            return -1
        elif not self.has_food and item.has_food:
            return 1
        else:
            return int.__cmp__(len(self.food_positions), len(item.food_positions))

    def __hash__(self):
        return hash((self.position, self.has_food, len(self.food_positions)))

    def __repr__(self):
        return '[ pos = ' + repr(self.position) + ' food = ' + repr(len(self.food_positions)) + ' food = ' + repr(self.has_food) +' ]'

    def go_up(self):
        position = self.position
        new_position = (position[ 0 ] - 1, position[ 1 ])
        return PacmanProblemState(new_position, self.food_positions)

    def go_down(self):
        position = self.position
        new_position = (position[ 0 ] + 1, position[ 1 ])
        return PacmanProblemState(new_position, self.food_positions)

    def go_right(self):
        position = self.position
        new_position = (position[ 0 ], position[ 1 ] + 1)
        return PacmanProblemState(new_position, self.food_positions)

    def go_left(self):
        position = self.position
        new_position = (position[ 0 ], position[ 1 ] - 1)
        return PacmanProblemState(new_position, self.food_positions)

    def eat(self):
        if self.has_food:
            food_positions = self.food_positions.copy()
            food_positions.remove(self.position)
            if len(food_positions) < 10:
                print('ATE at', self.position, len(food_positions), 'remaining')
            return PacmanProblemState(self.position, food_positions)
        else:
            return self

class Heuristic:
    @staticmethod
    def manhattan_distance(point_a, point_b):
        return math.fabs(point_a[ 0 ] - point_b[ 0 ]) + math.fabs(point_a[ 1 ] - point_b[ 1 ])

    @staticmethod
    def euclidean_distance(point_a, point_b):
        return math.sqrt((point_a[ 0 ] - point_b[ 0 ])**2 + (point_a[ 1 ] - point_b[ 1 ])**2)

    @staticmethod
    def closest_node(node, nodes):
        distances = [ (x, Heuristic.euclidean_distance(node, x)) for x in nodes ]
        compare = lambda x: x[ 1 ]
        closest = min(distances, key=compare)
        return closest

    # this is not admissible :(
    @staticmethod
    def manhattan_perimeter(initial_position, other_positions):
        current = initial_position
        positions = other_positions[:]
        distance = 0
        while len(positions) > 0:
            closest = Heuristic.closest_node(current, positions)
            distance += closest[ 1 ]
            if current in positions:
                positions.remove(current)
            current = closest[ 0 ]
        return distance

    @staticmethod
    def chebyshev_distance(initial_position, original_vertices):
        vertices = original_vertices[:]
        vertices.append(initial_position)
        distance = 0
        for x_i in vertices:
            for y_i in vertices:
                chebyshev_i = max(math.fabs(x_i[ 0 ] - y_i[ 0 ]), math.fabs(x_i[ 1 ] - y_i[ 1 ]))
                if chebyshev_i < distance:
                    distance = chebyshev_i
        return distance

    @staticmethod
    def minimum_spanning_tree(initial_position, vertices):
        # for vertex_a in vertices:
        #     row = distances_memory[ vertex_a ]
        #     distances_memory[ vertex_a ][ initial_position ] = Heuristic.manhattan_distance(vertex_a, initial_position)
        #     if initial_position not in distances_memory:
        #         distances_memory[ initial_position ] = {}
        #     distances_memory[ initial_position ][ vertex_a ] = distances_memory[ vertex_a ][ initial_position ]

        msts_key = repr(vertices)
        if msts_key in msts_memory:
            return msts_memory[ msts_key ]

        weights = {}
        parents = {}
        in_mst = set()

        initial_vertex = min(vertices)
        queue = PriorityQueue()
        queue.put((0, initial_vertex))
        weights[ initial_vertex ] = 0

        while not queue.empty():
            _, current = queue.get()
            in_mst.add(current)

            for vertex in vertices:
                weight = distances_memory[ current ][ vertex ]
                stored_weight = weights.get(vertex, float('inf'))
                if vertex not in in_mst and stored_weight > weight:
                    weights[ vertex ] = weight
                    queue.put((weight, vertex))
                    parents[ vertex ] = current
        msts_memory[ msts_key ] = parents
        return parents

    @staticmethod
    def distance_to_closest(pivot_position, positions):
        distances = set()
        if pivot_position not in distances_memory:
            distances_memory[ pivot_position ] = {}
        for position in positions:
            if position not in distances_memory[ pivot_position ]:
                distances_memory[ pivot_position ][ position ] = Heuristic.manhattan_distance(pivot_position, position)
            distances.add(distances_memory[ pivot_position ][ position ])
        return min(distances)


    @staticmethod
    def minimum_spanning_tree_perimeter(initial_position, original_vertices):
        mst = Heuristic.minimum_spanning_tree(initial_position, original_vertices)
        distance = 0
        for vertex in mst:
            distance += distances_memory[ mst[ vertex ] ][ vertex ]
        return distance + Heuristic.distance_to_closest(initial_position, original_vertices)


class PacmanProblem:
    def __init__(self):
        self.initial_state = 0

    def actions(self, state):
        actions = []
        position = state.position

        if state.has_food:
            return [ Action.EAT ]

        right_cell = self.maze[ position[ 0 ] ][ position[ 1 ] + 1 ]
        left_cell = self.maze[ position[ 0 ] ][ position[ 1 ] - 1 ]
        up_cell = self.maze[ position[ 0 ] - 1 ][ position[ 1 ] ]
        down_cell = self.maze[ position[ 0 ] + 1][ position[ 1 ] ]

        if left_cell == PATH or left_cell == INITIAL_POSITION_INDICATOR:
            actions.append(Action.GO_LEFT)

        if up_cell == PATH or up_cell == INITIAL_POSITION_INDICATOR:
            actions.append(Action.GO_UP)

        if right_cell == PATH or right_cell == INITIAL_POSITION_INDICATOR:
            actions.append(Action.GO_RIGHT)

        if down_cell == PATH or down_cell == INITIAL_POSITION_INDICATOR:
            actions.append(Action.GO_DOWN)

        if right_cell == FOOD_PELLET:
            actions.append(Action.GO_RIGHT)

        if down_cell == FOOD_PELLET:
            actions.append(Action.GO_DOWN)

        if left_cell == FOOD_PELLET:
            actions.append(Action.GO_LEFT)

        if up_cell == FOOD_PELLET:
            actions.append(Action.GO_UP)

        return actions

    def goal_test(self, state):
        return len(state.food_positions) == 0

    def initialize_distances_memory(self):
        vertices = self.food_positions
        for vertex_a in vertices:
            if vertex_a not in distances_memory:
                distances_memory[ vertex_a ] = {}
            row = distances_memory[ vertex_a ]
            for vertex_b in vertices:
                if vertex_b in row:
                    continue
                else:
                    distances_memory[ vertex_a ][ vertex_b ] = Heuristic.manhattan_distance(vertex_a, vertex_b)
                    if vertex_b not in distances_memory:
                        distances_memory[ vertex_b ] = {}
                    distances_memory[ vertex_b ][ vertex_a ] = distances_memory[ vertex_a ][ vertex_b ]

    def load(self, filepath):
        file_object = open(filepath, 'r')
        text = file_object.read()
        # last line is an empty newline so we remove it.
        lines = text.split('\n')[:-1]
        column_count = len(lines[ 0 ])
        self.maze = [ [char for char in line] for line in lines ]

        # for printing
        self.maze_copy = copy.deepcopy(self.maze)

        self.food_positions = set([
            (pos / column_count, pos % column_count)
            for pos
            in list(find_all_occurrences(FOOD_PELLET, text.replace('\n', '')))
        ])

        self.initialize_distances_memory()

        absolute_position = text.replace('\n', '').index(INITIAL_POSITION_INDICATOR)
        initial_position = (absolute_position / column_count, absolute_position % column_count)
        self.initial_state =  PacmanProblemState(initial_position, self.food_positions)

    def result(self, state, action):
        if action == Action.GO_UP:
            return state.go_up()
        elif action == Action.GO_DOWN:
            return state.go_down()
        elif action == Action.GO_RIGHT:
            return state.go_right()
        elif action == Action.GO_LEFT:
            return state.go_left()
        elif action == Action.EAT:
            return state.eat()
        else:
            return state

    def step_cost(self, state, action):
        if action == Action.EAT:
            return 0
        return 1

    def estimated_cost(self, state):
        return Heuristic.minimum_spanning_tree_perimeter(state.position, state.food_positions)

    def print_solution_path(self, node):
        if node == None:
            return
        current_node = node
        while current_node.parent != None:
            position = current_node.state.position
            self.maze_copy[ position[ 0 ] ][ position[ 1 ] ] = SELECTED_PATH
            current_node = current_node.parent

        for line in self.maze_copy:
            for char in line:
                if (char == SELECTED_PATH):
                    print(TerminalColor.RED.value + char, end='')
                elif char not in [ WALL ]:
                    print(TerminalColor.BLUE.value + char, end='')
                else:
                    print(TerminalColor.DEFAULT.value + char, end='')
            print('')

if __name__ == '__main__':
    # I'll use this for tiebreaking
    no_food_state = PacmanProblemState((0,0))
    food_state = PacmanProblemState((0, 0), set([ (0,0), (1,1) ]))
    print('food is more than important than no food:', food_state.__cmp__(no_food_state) == -1)

    other_food_state = PacmanProblemState((0, 0), set([ (0,0), (1,1), (1,2) ]))
    print('less food positions better than more food positions', food_state.__cmp__(other_food_state) == -1)
    print('------------------------')

    from Queue import PriorityQueue
    queue = PriorityQueue()
    queue.put((1, food_state))
    print('inserted prio 1 with food')
    queue.put((0, other_food_state))
    print('inserted prio 0 w food')
    queue.put((1, no_food_state))
    print('inserted prio 1 w/o food')
    queue.put((99, food_state))

    print('other_food_state should go first', queue.get() == (0, other_food_state))
    print('food_state should go next', queue.get() == (1, food_state))
    print('no_food_state should go last', queue.get() == (1, no_food_state))
