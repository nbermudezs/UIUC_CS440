from __future__ import print_function

from queue import *
from search_enums import *

import copy
import math

priority_matrix = {}
evaluation_memory = {}

class Node:
    def __init__(self, state, parent, action, path_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __eq__(self, item):
        return type(item) == Node and self.state == item.state

    def __ne__(self, item):
        return type(item) != Node or self.state != item.state

    def __lt__(self, item):
        return self.state < item.state

    def __cmp__(self, item):
        cmp = self.state.__cmp__(item.state)
        if cmp == 0:
            return int.__cmp__(self.path_cost, item.path_cost)
        return cmp

    def __hash__(self):
        return hash(self.state)

    def __repr__(self):
        result = ''
        if self.parent != None:
            result = repr(self.parent)
        if self.action != None:
            result += '\n' + str(self.action) + ' to ' + repr(self.state)
        if self.path_cost:
            result += ' => C = ' + repr(self.path_cost)
        return result


class SearchResult:
    def __init__(self, expanded_nodes = 0, leaf_node = None):
        self.expanded_nodes = expanded_nodes
        self.leaf_node = leaf_node
        self.path_cost = leaf_node.path_cost if leaf_node != None else 0

class SearchProblemSolver:
    def __init__(self, strategy):
        self.strategy = strategy
        priority_matrix = {}

    def initialize_frontier(self):
        if self.strategy == SearchStrategy.BFS:
            return Queue()
        elif self.strategy == SearchStrategy.DFS:
            return LifoQueue()
        elif self.strategy == SearchStrategy.GBFS:
            return PriorityQueue()
        elif self.strategy == SearchStrategy.A_STAR:
            return PriorityQueue()
        else:
            return None

    def child_node(self, problem, parent, action):
        state = problem.result(parent.state, action)
        path_cost = parent.path_cost + problem.step_cost(parent.state, action)
        return Node(state, parent, action, path_cost)

    def evaluate(self, problem, node):
        h = problem.estimated_cost
        if self.strategy == SearchStrategy.GBFS:
            return h(node.state)
        elif self.strategy == SearchStrategy.A_STAR:
            if node.state not in evaluation_memory:
                evaluation_memory[ node.state ] = h(node.state)
            return node.path_cost + evaluation_memory[ node.state ]
        else:
            return 0

    def graph_search(self, problem):
        node = Node(problem.initial_state, None, None, 0)
        if problem.goal_test(node.state):
            return SearchResult(0, node)

        frontier = self.initialize_frontier()
        if frontier is None:
            return SearchResult()
        frontier.put((0, node))

        explored = set()
        frontier_set = set()
        frontier_set.add(node)

        while not frontier.empty():
            _, node = frontier.get()
            frontier_set.remove(node)

            if problem.goal_test(node.state):
                return SearchResult(len(explored), node)

            previous_priority = priority_matrix.get(node.state, float('inf'))
            if node.state.priority > previous_priority:
                continue

            explored.add(node.state)
            frontier_set.add(node)
            for action in problem.actions(node.state):
                child = self.child_node(problem, node, action)
                child_already_in_frontier = child in frontier_set

                if not child_already_in_frontier and child.state not in explored:
                    priority = self.evaluate(problem, child)
                    frontier.put((priority, child))
                    frontier_set.add(child)
                elif child_already_in_frontier:
                    priority = self.evaluate(problem, child)
                    previous_priority = priority_matrix.get(child, float('inf'))
                    if priority < previous_priority:
                        priority_matrix[ child ] = priority
                        frontier.put((priority, child))

        return SearchResult()

    def solve(self, problem):
        return self.graph_search(problem)

if __name__ == '__main__':
    pass
