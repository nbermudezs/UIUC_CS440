from search_enums import *

from maze_problem import MazeProblem
from pacman_problem import PacmanProblem, Heuristic
from search_problem_solver import SearchProblemSolver

import time

def print_action_sequence(leaf):
    sequence = []
    node = leaf
    while node != None:
        sequence.append(node)
        node = node.parent

    sequence = reversed(sequence)
    for node in sequence:
        print(node)

if __name__ == '__main__':
    # possible values: see search_enums.py
    strategy = SearchStrategy.A_STAR

    # if multipellet is set to False it will force the solver to use
    # Manhattan distance as the heuristic
    multipellet = True

    # name of the file under the 'input' folder
    maze = 'tiny_with_dots'

    # chosen heuristic to use for multipellet problem.
    # use either Heuristic.minimum_spanning_tree_perimeter for optimal
    # or Heuristic.relaxed_christofides for suboptimal cost
    h = Heuristic.minimum_spanning_tree_perimeter

    # setup puzzle and solver
    solver = SearchProblemSolver(strategy)
    problem = PacmanProblem(h) if multipellet else MazeProblem()
    problem.load('./input/' + maze + '.txt')


    start_time = time.clock()

    import cProfile, pstats, io
    pr = cProfile.Profile()
    pr.enable()

    # run Forrest, run!
    result = solver.solve(problem)

    pr.disable()
    s = io.StringIO()
    sortby = 'cumtime'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

    elapsed_time = time.clock() - start_time
    if result:
        print(strategy, 'expanded', result.expanded_nodes, 'nodes and a path cost', result.path_cost)
        problem.print_solution_path(result.leaf_node)
        print_action_sequence(result.leaf_node)
        print('Took', elapsed_time, 'to complete')
