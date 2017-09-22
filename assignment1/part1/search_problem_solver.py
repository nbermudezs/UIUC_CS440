from __future__ import print_function

from Queue import *
from search_enums import *

import copy
import math

priority_matrix = {}

class Node:
    def __init__(self, state, parent, action, path_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __eq__(self, item):
        return item != None and self.state == item.state

    def __ne__(self, item):
        return item == None or self.state != item.state

    def __cmp__(self, item):
        cmp = self.state.__cmp__(item.state)
        if cmp == 0:
            return int.__cmp__(self.path_cost, item.path_cost)
        return cmp

    def __hash__(self):
        return hash(hash(self.state) + hash(self.action) + hash(self.path_cost))

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
        if self.strategy == SearchStrategy.GBFS:
            return problem.estimated_cost(node.state)
        elif self.strategy == SearchStrategy.A_STAR:
            return node.path_cost + problem.estimated_cost(node.state)
        else:
            return 0

    def graph_search(self, problem):
        goal_node = None
        node = Node(problem.initial_state, None, None, 0)
        if problem.goal_test(node.state):
            return SearchResult(0, node)

        frontier = self.initialize_frontier()
        if frontier is None:
            return SearchResult()
        frontier.put((0, node))

        explored = set()
        frontier_set = set()

        while not goal_node:
            if frontier.empty():
                return SearchResult()

            _, node = frontier.get()

            # START TEST:
            # previous_priority = priority_matrix.get(node.state, float('inf'))
            # if node.state.priority > previous_priority:
            #     continue
            # END TEST

            explored.add(node.state)
            frontier_set.add(node)

            for action in problem.actions(node.state):
                child = self.child_node(problem, node, action)

                # START TEST:
                # if problem.goal_test(child.state):
                #     goal_node = child
                #     break
                # priority = self.evaluate(problem, child)
                # frontier.put((priority, child))
                # child.priority = priority
                # priority_matrix[ child ] = priority
                # END TEST

                if child not in frontier_set and child.state not in explored:
                    if problem.goal_test(child.state):
                        goal_node = child
                        break
                    priority = self.evaluate(problem, child)
                    frontier.put((priority, child))
                    frontier_set.add(child)
        return SearchResult(len(explored), goal_node)

    def solve(self, problem):
        return self.graph_search(problem)

if __name__ == '__main__':
    pass
