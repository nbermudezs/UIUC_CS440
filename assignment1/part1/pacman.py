from __future__ import print_function

from Queue import *
from node import Node
from search_enums import *

import copy
import math
import re

CURRENT_POSITION_INDICATOR = 'P'
FOOD_PELLET = '.'
SELECTED_PATH = '.'
PATH = ' '
WALL = '%'

def manhattan_distance(pointA, pointB):
    return math.fabs(pointA[ 0 ] - pointB[ 0 ]) + math.fabs(pointA[ 1 ] - pointB[ 1 ])

def find_all_occurrences(pattern, text):
    i = text.find(pattern)
    while i != -1:
        yield i
        i = text.find(pattern, i + 1)

class PacmanSolver:
    def __init__(self):
        self.maze = []
        self.position = (0, 0)
        self.dot_ascii_code = 49

    def load(self, filepath):
        file_object = open(filepath, 'r')
        text = file_object.read()
        lines = text.split('\n')[:-1]
        column_count = len(lines[ 0 ])
        self.maze = [ [char for char in line] for line in lines ]
        self.original_maze = copy.deepcopy(self.maze)
        absolute_position = text.replace('\n', '').index(CURRENT_POSITION_INDICATOR)
        self.position = (absolute_position / column_count, absolute_position % column_count)

        self.goal_positions = [
            (pos / column_count, pos % column_count)
            for pos
            in list(find_all_occurrences(FOOD_PELLET, text.replace('\n', '')))
        ]

    def transition(self, state, action):
        if action == Action.GO_UP:
            return (state[ 0 ], state[ 1 ] - 1)
        elif action == Action.GO_DOWN:
            return (state[ 0 ], state[ 1 ] + 1)
        elif action == Action.GO_LEFT:
            return (state[ 0 ] - 1, state[ 1 ])
        elif action == Action.GO_RIGHT:
            return (state[ 0 ] + 1, state[ 1 ])
        else:
            return state

    def is_food_pellet(self, position):
        return position in self.goal_positions

    def mark_as_eaten(self, position):
        self.goal_positions.remove(position)
        self.maze[ position[ 0 ] ][ position[ 1 ]] = PATH

    def is_done(self):
        return len(self.goal_positions) == 0

    def get_dot_id(self):
        if self.dot_ascii_code > 122:
            return '#'
        code = self.dot_ascii_code
        self.dot_ascii_code += 1
        if self.dot_ascii_code == 91:
            self.dot_ascii_code = 97
        elif self.dot_ascii_code == 58:
            self.dot_ascii_code = 65
        return chr(code)

    def tree_search(self, child_picking_heuristic):
        solution_leaves = []
        root = Node(self.position, self.maze[ 0 ][ 0 ])
        current_node = root
        self.frontier.put((0, root))

        while not self.frontier.empty():
            frontier_item = self.frontier.get()
            current_node = frontier_item[ 1 ]
            if current_node.parent != None:
                current_node.path_cost = current_node.parent.path_cost + self.path_cost(current_node.parent, current_node)

            node_position = current_node.position
            has_food = self.is_food_pellet(node_position)
            if has_food:
                self.mark_as_eaten(node_position)
                solution_leaves.append(current_node)
            if self.is_done():
                break

            if (frontier_item[ 0 ], node_position) not in self.explored:
                self.explored[ (frontier_item[ 0 ], node_position) ] = True
                children = [
                    (0, self.transition(node_position, Action.GO_LEFT)),
                    (0, self.transition(node_position, Action.GO_UP)),
                    (0, self.transition(node_position, Action.GO_RIGHT)),
                    (0, self.transition(node_position, Action.GO_DOWN))
                ]

                for child_info in child_picking_heuristic(current_node, children):
                    priority = child_info[ 0 ]
                    child_position = child_info[ 1 ]
                    cell_type = self.maze[ child_position[ 0 ] ][ child_position[ 1 ] ]
                    if cell_type != WALL and child_info not in self.explored:
                        child_node = Node(child_position, cell_type)
                        current_node.append(child_node)
                        self.frontier.put((priority, child_node))
        path_cost = 0
        for index, leaf in enumerate(solution_leaves):
            node = leaf
            while node.parent is not None:
                path_cost += 1
                position = node.position
                if node.position == leaf.position:
                    self.maze[ position[ 0 ] ][ position[ 1 ] ] = self.get_dot_id()
                elif node.cell_type == PATH:
                    self.maze[ position[ 0 ] ][ position[ 1 ] ] = SELECTED_PATH
                node = node.parent
        self.stats[ 'path_cost' ] = path_cost
        self.stats[ 'expanded_nodes' ] = len(self.explored)
        return path_cost

    def bfs(self):
        self.frontier = LifoQueue()
        return self.tree_search(lambda current_node, children: children)

    def dfs(self):
        self.frontier = Queue()
        return self.tree_search(lambda current_node, children: children)

    def a_star(self):
        self.frontier = PriorityQueue()
        return self.tree_search(self.a_star_heuristic)

    def gbfs(self):
        self.frontier = PriorityQueue()
        return self.tree_search(self.gbfs_heuristic)

    def a_star_heuristic(self, current_node, children):
        goal_position = self.closest_goal(current_node)

        prioritized_actions = []
        for _, position in children:
            g_n = current_node.path_cost + self.path_cost(current_node, position)
            h_n = manhattan_distance(goal_position, position)
            f_n = g_n + h_n
            prioritized_actions.append((f_n, position))
        return prioritized_actions

    def gbfs_heuristic(self, current_node, children):
        goal_position = self.closest_goal(current_node)
        prioritized_actions = []
        for _, position in children:
            distance = manhattan_distance(goal_position, position)
            prioritized_actions.append((distance, position))
        return prioritized_actions

    def closest_goal(self, node):
        position = node.position
        return sorted([
            (goal, manhattan_distance(position, goal))
            for goal in self.goal_positions
        ], lambda a, b: cmp(a[ 1 ], b[ 1 ]))[ 0 ][ 0 ]

    def path_cost(self, origin, destination):
        return 1

    def reset_statistics(self):
        self.stats = {
            'expanded_nodes': 0,
            'path_cost': 0
        }

    def reset_data_structures(self):
        self.maze = copy.deepcopy(self.original_maze)
        self.explored = {}
        self.tree = []
        self.solution_path = []

    def solve(self, strategy, heuristic = None):
        self.strategy = strategy

        self.reset_statistics()
        self.reset_data_structures()

        if strategy == SearchStrategy.A_STAR:
            self.a_star()
        elif strategy == SearchStrategy.BFS:
            self.bfs()
        elif strategy == SearchStrategy.DFS:
            self.dfs()
        elif strategy == SearchStrategy.GBFS:
            self.gbfs()

    def print_maze(self):
        for line in self.maze:
            for char in line:
                if (char == SELECTED_PATH):
                    print(TerminalColor.RED.value + char, end='')
                elif char not in [ WALL ]:
                    print(TerminalColor.BLUE.value + char, end='')
                else:
                    print(TerminalColor.DEFAULT.value + char, end='')
            print('')

    def report_statistics(self):
        print('Solved maze using ', self.strategy)
        self.print_maze()
        print('Path cost:', self.stats[ 'path_cost' ])
        print('# of expanded nodes:', self.stats[ 'expanded_nodes' ])
        print('===============================================================')
