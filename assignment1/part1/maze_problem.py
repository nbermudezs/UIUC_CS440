from __future__ import print_function
from bitarray import bitarray
from search_enums import *

import heapq
import pdb

class PriorityQueue:
    def __init__(self):
        self.items = []

    def put(self, item):
        heapq.heappush(self.items, item)

    def get(self):
        return heapq.heappop(self.items)

    def empty(self):
        return len(self.items) == 0

import copy
import functools
import math

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

class MazeProblemState:
    def __init__(self, position, food_state, problem):
        self.problem = problem
        self.position = position
        self.food_state = food_state
        self.priority = 0

    def __eq__(self, item):
        return self.position == item.position and \
                self.food_state == item.food_state

    def __ne__(self, item):
        return self.position != item.position or \
                self.food_state != item.food_state

    def __lt__(self, item):
        if self.food_state.count(0) == item.food_state.count(0):
            return self.position < item.position
        return self.food_state.count(0) < item.food_state.count(0)

    def __hash__(self):
        return hash((self.position, self.food_state.to01()))

    def __repr__(self):
        return '(' + str(self.position) + ':' + self.food_state.to01() + ')'

    def __str__(self):
        return '[ pos = ' + repr(self.position) + '\tremaining = ' + repr(self.food_state.count(0)) + '\tfood state = ' + repr(self.food_state) +' ]'

    def go_up(self):
        position = self.position
        new_position = (position[ 0 ] - 1, position[ 1 ])
        return self.move_to(new_position)

    def go_down(self):
        position = self.position
        new_position = (position[ 0 ] + 1, position[ 1 ])
        return self.move_to(new_position)

    def go_right(self):
        position = self.position
        new_position = (position[ 0 ], position[ 1 ] + 1)
        return self.move_to(new_position)

    def go_left(self):
        position = self.position
        new_position = (position[ 0 ], position[ 1 ] - 1)
        return self.move_to(new_position)

    def move_to(self, new_position):
        index = self.problem.food_order.get(new_position, -1)
        food_state = self.food_state
        if index > -1 and not food_state[ index ]:
            food_state = bitarray(self.problem.food_count)
            food_state.setall(0)
            food_state[ index ] = 1
            food_state = self.food_state | food_state
        return MazeProblemState(new_position, food_state, self.problem)

class Heuristic:
    @staticmethod
    def manhattan_distance(point_a, point_b):
        return math.fabs(point_a[ 0 ] - point_b[ 0 ]) + math.fabs(point_a[ 1 ] - point_b[ 1 ])

class MazeProblem:
    def __init__(self):
        self.initial_state = 0
        distances_memory = {}
        msts_memory = {}

    def actions(self, state):
        actions = []
        position = state.position

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
        return state.food_state.count(0) == 0

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

        self.food_positions = [
            (pos // column_count, pos % column_count)
            for pos
            in list(find_all_occurrences(FOOD_PELLET, text.replace('\n', '')))
        ]
        self.food_count = len(self.food_positions)
        self.food_order = {}
        positions = self.food_positions[:]
        while len(positions):
            first = min(positions)
            self.food_order[ first ] = len(self.food_order)
            positions.remove(first)
        food_state = bitarray(self.food_count)
        food_state.setall(0)

        self.initialize_distances_memory()

        absolute_position = text.replace('\n', '').index(INITIAL_POSITION_INDICATOR)
        initial_position = (absolute_position // column_count, absolute_position % column_count)
        self.initial_state =  MazeProblemState(initial_position, food_state, self)

    def result(self, state, action):
        if action == Action.GO_UP:
            return state.go_up()
        elif action == Action.GO_DOWN:
            return state.go_down()
        elif action == Action.GO_RIGHT:
            return state.go_right()
        elif action == Action.GO_LEFT:
            return state.go_left()
        else:
            return state

    def step_cost(self, state, action):
        return 1

    @functools.lru_cache(maxsize=1024)
    def estimated_cost(self, state):
        goal_position = None
        for i, eaten in enumerate(state.food_state):
            if not eaten:
                goal_position = state.problem.food_positions[ i ]
                break
        if not goal_position:
            return 0
        return Heuristic.manhattan_distance(state.position, goal_position)

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
