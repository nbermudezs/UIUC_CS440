from __future__ import print_function
from bitarray import bitarray
from search_enums import *

import heapq

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

class PacmanProblemState:
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
        return PacmanProblemState(new_position, food_state, self.problem)

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
    def minimum_spanning_tree(initial_position, vertices, msts_key):
        # for vertex_a in vertices:
        #     row = distances_memory[ vertex_a ]
        #     distances_memory[ vertex_a ][ initial_position ] = Heuristic.manhattan_distance(vertex_a, initial_position)
        #     if initial_position not in distances_memory:
        #         distances_memory[ initial_position ] = {}
        #     distances_memory[ initial_position ][ vertex_a ] = distances_memory[ vertex_a ][ initial_position ]

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
    def minimum_spanning_tree_perimeter(initial_position, original_vertices, key):
        if len(original_vertices) == 0:
            return 0

        mst = Heuristic.minimum_spanning_tree(initial_position, original_vertices, key.to01())
        distance = 0
        for vertex in mst:
            distance += distances_memory[ mst[ vertex ] ][ vertex ]
        return distance + Heuristic.distance_to_closest(initial_position, original_vertices)

    @staticmethod
    def relaxed_christofides(initial_position, original_vertices, key):
        return 2 * Heuristic.minimum_spanning_tree_perimeter(initial_position, original_vertices, key)

class PacmanProblem:
    def __init__(self, heuristic = Heuristic.minimum_spanning_tree_perimeter):
        self.initial_state = 0
        self.heuristic = heuristic

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
        self.initial_state =  PacmanProblemState(initial_position, food_state, self)

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
        vertices = set()
        for i, eaten in enumerate(state.food_state):
            if not eaten:
                vertices.add(state.problem.food_positions[ i ])
        return self.heuristic(state.position, vertices, state.food_state)

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
