import pdb
import time

from functools import cmp_to_key
from .player import Player

inf = float('inf')

class Util:
    def print_board(board, rows, cols):
        import math, sys
        format = '%s'

        print('next to move', board.next_to_move)

        for i in range(rows):
            sep = '['
            for j in range(cols):
                val = ' '
                if board.whites[ i * cols + j ]:
                    val = 'W'
                elif board.blacks[ i * cols + j ]:
                    val = 'B'
                formatted = (format % val)
                sys.stdout.write(sep + formatted)
                sep = ', '
            sys.stdout.write(']\n')

class AlphaBetaPlayer(Player):
    def __init__(self, heuristic = None, max_depth = 4, sort_actions = False):
        Player.__init__(self)
        self.heuristic = heuristic
        self.max_depth = max_depth
        self.sort_actions = sort_actions

    def _maximize(self, game, state, alpha, beta, depth):
        self.current_move_node_count += 1
        local_start = time.clock()
        if game.terminal_test(state) or depth >= self.max_depth:
            return self.heuristic(game, state)

        if self.sort_actions:
            func = lambda a,b: self.heuristic(game, game.result(state, a)) - self.heuristic(game, game.result(state, b))
            actions = sorted(game.actions(state), key = cmp_to_key(func))
        else:
            actions = game.actions(state)

        value = inf
        for action in actions:
            value = self._minimize(game, game.result(state, action), alpha, beta, depth + 1)
            # Util.print_board(state, 8, 8)
            # Util.print_board(game.result(state, action), 8, 8)
            # print('max: ', alpha, 'value', value)
            if value >= beta:
                return value
            alpha = max(value, alpha)
        return value

    def _minimize(self, game, state, alpha, beta, depth):
        self.current_move_node_count += 1
        if game.terminal_test(state) or depth >= self.max_depth:
            return self.heuristic(game, state)

        if self.sort_actions:
            func = lambda a,b: self.heuristic(game, game.result(state, a)) - self.heuristic(game, game.result(state, b))
            actions = sorted(game.actions(state), key = cmp_to_key(func))
        else:
            actions = game.actions(state)

        value = inf
        for action in actions:
            value = self._maximize(game, game.result(state, action), alpha, beta, depth + 1)
            # Util.print_board(state, 8, 8)
            # Util.print_board(game.result(state, action), 8, 8)
            # print('min: ', alpha, 'value', value)
            if value <= alpha:
                return value
            beta = min(value, beta)
        return value


    def choose_move(self, game, state):
        # for bookkeeping
        self.current_move_node_count = 0
        start = time.clock()

        best = -inf
        chosen_action = None

        func = lambda a,b: self.heuristic(game, game.result(state, a)) - self.heuristic(game, game.result(state, b))
        actions = sorted(game.actions(state), key = cmp_to_key(func))
        # actions = game.actions(state)

        for action in actions:
            # if game.terminal_test(game.result(state, action))
            value = self._minimize(game, game.result(state, action), best, inf, 0)
            # Util.print_board(state, 8, 8)
            # Util.print_board(game.result(state, action), 8, 8)
            # print('value: ', value, 'best so far', best)
            # pdb.set_trace()
            if value > best:
                best = value
                chosen_action = action
        self.move_count += 1
        self.time_to_move.append(time.clock() - start)
        self.expanded_nodes.append(self.current_move_node_count)
        # pdb.set_trace()
        return chosen_action

    def __repr__(self):
        return 'AlphaBetaPlayer(moves made=' + str(self.move_count) + \
            ', avg time to move=' + \
            str(sum(self.time_to_move) / len(self.time_to_move)) + \
            ', avg expanded nodes=' + \
            str(sum(self.expanded_nodes) / len(self.expanded_nodes)) + \
            ', total expanded nodes=' + str(sum(self.expanded_nodes)) + ')'
