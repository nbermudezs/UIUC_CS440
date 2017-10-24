import pdb
import time

from .player import Player

inf = float('inf')

class MinimaxPlayer(Player):
    def __init__(self, heuristic = None, max_depth = 3):
        Player.__init__(self)
        self.heuristic = heuristic
        self.max_depth = max_depth

    def _maximize(self, game, state, depth):
        self.current_move_node_count += 1
        if game.terminal_test(state):
            return game.utility(state, game.player_to_move(state))
        if depth >= self.max_depth:
            return self.heuristic(game, state)
        return max([ self._minimize(game, game.result(state, action), depth + 1) for action in game.actions(state) ])

    def _minimize(self, game, state, depth):
        self.current_move_node_count += 1
        if game.terminal_test(state):
            return game.utility(state, game.player_to_move(state))
        if depth >= self.max_depth:
            return self.heuristic(game, state)
        return min([ self._maximize(game, game.result(state, action), depth + 1) for action in game.actions(state) ])


    def choose_move(self, game, state):
        # for bookkeeping
        self.current_move_node_count = 0
        start = time.clock()

        best = -inf
        chosen_action = None
        for action in game.actions(state):
            value = self._minimize(game, game.result(state, action), 1)
            if value > best:
                best = value
                chosen_action = action
        self.move_count += 1
        self.time_to_move.append(time.clock() - start)
        self.expanded_nodes.append(self.current_move_node_count)
        return chosen_action

    def __repr__(self):
        return 'MinimaxPlayer(moves made=' + str(self.move_count) + \
            ', avg time to move=' + \
            str(sum(self.time_to_move) / len(self.time_to_move)) + \
            ', avg expanded nodes=' + \
            str(sum(self.expanded_nodes) / len(self.expanded_nodes)) + \
            ', total expanded nodes=' + str(sum(self.expanded_nodes)) + ')'
