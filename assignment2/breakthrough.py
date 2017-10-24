__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

import pdb

from bitarray import bitarray
from collections import namedtuple, defaultdict
from game import Game
from copy import deepcopy
from enums import PlayerName

PAWN_ROW_COUNT = 2
ONE = bitarray('1')

Position = namedtuple('Position', [ 'origin', 'destination' ])

class BreakthroughBoardPiece:
    def __init__(self, position, player):
        self.position = position
        self.player = player
        self.protected_value = 0
        self.attacked_value = 0
        self.has_row_neighbors = False
        self.has_col_neighbors = False

class BreakthroughBoard:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.next_to_move = PlayerName.WHITES
        self._create_maze()
        self.value = 0

    def _create_maze(self):
        self.whites = bitarray(self.cols * self.rows)
        self.blacks = bitarray(self.cols * self.rows)

        self.whites.setall(False)
        self.blacks.setall(False)
        for i in range(self.cols * PAWN_ROW_COUNT):
            self.whites[ i ] = True
            self.blacks[ -i - 1 ] = True

    def move(self, origin, to):
        clone = deepcopy(self)
        if self.next_to_move == PlayerName.WHITES:
            # only move if there was something to move
            if not self.whites[ origin ]:
                return self

            # it is capturing black
            if self.blacks[ to ]:
                clone.blacks[ to ] = False

            clone.whites[ to ] = True
            clone.whites[ origin ] = False
            clone.next_to_move = PlayerName.BLACKS
        elif self.next_to_move == PlayerName.BLACKS:
            # only move if there was something to move
            if not self.blacks[ origin ]:
                return self

            # it is capturing white
            if self.whites[ to ]:
                clone.whites[ to ] = False

            clone.blacks[ to ] = True
            clone.blacks[ origin ] = False
            clone.next_to_move = PlayerName.WHITES
        return clone

    def remaining_whites(self):
        return self.whites.count(True)

    def remaining_blacks(self):
        return self.blacks.count(True)

    def __repr__(self):
        return self.whites.to01() + '\n' + self.blacks.to01()

class Breakthrough(Game):
    def __init__(self, rows = 8, columns = 8):
        self.rows = rows
        self.cols = columns
        self.size = rows * columns
        self.initial_board_state = BreakthroughBoard(rows, columns)
        self.board_state = BreakthroughBoard(rows, columns)

    def _position_actions(self, state, position):
        player = self.player_to_move(state)
        positions = []
        if player == PlayerName.WHITES:
            in_front = position + self.cols
            if in_front >= self.size:
                return []
            if not state.blacks[ in_front ] and not state.whites[ in_front ]:
                # valid to move to the front cell
                positions.append(in_front)

            left = in_front - 1
            if left % self.cols != self.cols - 1:
                if not state.whites[ left ]:
                    # do not try to move to a cell ocupied by same player
                    positions.append(left)

            right = in_front + 1
            if right % self.cols != 0:
                if not state.whites[ right ]:
                    # do not try to move to a cell ocupied by same player
                    positions.append(right)
        else:
            in_front = position - self.cols
            if in_front < 0:
                return []
            if not state.blacks[ in_front ] and not state.whites[ in_front ]:
                # valid to move to the front cell
                positions.append(in_front)

            left = in_front - 1
            if left % self.cols != self.cols - 1:
                if not state.blacks[ left ]:
                    # do not try to move to a cell ocupied by same player
                    positions.append(left)

            right = in_front + 1
            if right % self.cols != 0:
                if not state.blacks[ right ]:
                    # do not try to move to a cell ocupied by same player
                    positions.append(right)
        return positions

    def actions(self, state):
        actions = []
        player = self.player_to_move(state)
        if player == PlayerName.WHITES:
            white_positions = state.whites.itersearch(ONE)
            for position in white_positions:
                for destination in self._position_actions(state, position):
                    actions.append(Position(position, destination))
        else:
            black_positions = state.blacks.itersearch(ONE)
            for position in black_positions:
                for destination in self._position_actions(state, position):
                    actions.append(Position(position, destination))
        return actions

    def result(self, state, move):
        return state.move(move.origin, move.destination)

    def terminal_test(self, state):
        if self.player_to_move(state) == PlayerName.WHITES:
            if state.blacks[ 0:self.cols ].any() or state.whites.count() == 0:
                return PlayerName.BLACKS
        else:
            if state.whites[ self.size - self.cols:self.size ].any() or state.blacks.count() == 0:
                return PlayerName.WHITES
        return False

    def display(self, state):
        pass

    def utility(self, state, player):
        if player == PlayerName.WHITES:
            return state.blacks[ self.size - self.cols:self.size ].count() * 1e11
        else:
            return state.whites[ 0:self.cols ].count() * 1e11

    def player_to_move(self, state):
        return state.next_to_move

    def play_game(self, *players):
        state = self.board_state
        print('initial board')
        Util.print_board(state, self.rows, self.cols)
        while True:
            for player in players:
                print(self.player_to_move(state), 'moves')
                move = player.choose_move(self, state)
                state = self.result(state, move)
                Util.print_board(state, self.rows, self.cols)
                print('\n\n')
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.player_to_move(self.initial_board_state))


class Breakthrough3WorkersToBase(Breakthrough):
    def terminal_test(self, state):
        if self.player_to_move(state) == PlayerName.WHITES:
            return state.blacks[ 0:self.cols ].count() == 3 or state.whites.count() <= 2
        else:
            return state.whites[ -self.cols - 1: -1 ].count() == 3 or state.blacks.count() <= 2

class Util:
    def print_bitarray_as_matrix(array, rows, cols):
        import math, sys
        width = 1
        format = ('%%%d' % width)

        for i in range(rows):
            sep = '['
            for j in range(cols):
                val = array[ i * cols + j ]
                formatted = ((format + 'd') % val)
                sys.stdout.write(sep + formatted)
                sep = ', '
            sys.stdout.write(']\n')

    def print_board(board, rows, cols):
        import math, sys
        format = '%s'

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

if __name__ == '__main__':
    """
    Test the board
    """
    board = BreakthroughBoard(8, 8)
    Util.print_bitarray_as_matrix(board.whites, 8, 8)
    print('\n\n')

    Util.print_board(board, 8, 8)
    print('\n\n')

    # move whites
    board.move(13, 29)
    Util.print_board(board, 8, 8)
    print('\n\n')

    # move blacks
    board.move(-12, -28)
    Util.print_board(board, 8, 8)
    print('\n\n')

    # white should capture black
    board.move(29, -28)
    Util.print_board(board, 8, 8)
    print('\n\n')

    # nothing should change.
    board.move(29, -28)
    Util.print_board(board, 8, 8)

    """
    Test the game
    """
    game = Breakthrough()
    is_terminal = game.terminal_test(board)
    print('is board in terminal state?', is_terminal)
    print('\n\n')

    valid_moves = game.actions(game.board_state)
    for move in valid_moves:
        print('[W] valid move:', move)
    print('\n\n')

    board.move(-1, 1)
    Util.print_board(board, 8, 8)
    is_terminal = game.terminal_test(board)
    print('is board in terminal state?', is_terminal)
    print('\n\n')

    game.board_state = game.board_state.move(11, 19)
    Util.print_board(game.board_state, 8, 8)
    valid_moves = game.actions(game.board_state)
    for move in valid_moves:
        print('[B] valid move:', move)
    print('\n\n')

    game.board_state = game.board_state.move(49, 40)
    Util.print_board(game.board_state, 8, 8)
    valid_moves = game.actions(game.board_state)
    for move in valid_moves:
        print('[W] valid move:', move)
    print('\n\n')

    """
    Test Breakthrough3WorkersToBase
    """
    game = Breakthrough3WorkersToBase(8, 8)
    game.board_state = game.board_state.move(4, 59)
    is_terminal = game.terminal_test(game.board_state)
    print('Is Breakthrough3WorkersToBase terminal with one pawn in base?', is_terminal)

    # blacks move
    game.board_state = game.board_state.move(48, 40)
    # whites move
    game.board_state = game.board_state.move(5, 56)
    is_terminal = game.terminal_test(game.board_state)
    print('Is Breakthrough3WorkersToBase terminal with two pawn in base?', is_terminal)

    # blacks move
    game.board_state = game.board_state.move(49, 41)
    # whites move
    game.board_state = game.board_state.move(12, 60)
    is_terminal = game.terminal_test(game.board_state)
    print('Is Breakthrough3WorkersToBase terminal with three pawn in base?', is_terminal)
