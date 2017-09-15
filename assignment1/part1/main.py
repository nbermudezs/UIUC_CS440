from maze import MazeSolver
from search_enums import *

import time

if __name__ == '__main__':
    # maze solvers
    mazes = [ 'medium', 'large', 'open' ]
    algorithms = [ SearchStrategy.BFS, SearchStrategy.DFS, SearchStrategy.GBFS, SearchStrategy.A_STAR ]

    for maze in mazes:
        for algorithm in algorithms:
            solver = MazeSolver()
            solver.load('./input/' + maze + '.txt')
            solver.solve(algorithm)
            solver.report_statistics()
            time.sleep(2)
