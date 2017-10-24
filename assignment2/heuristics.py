__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

import random
import pdb

from bitarray import bitarray
from enums import PlayerName

ARBITRARY_MULTIPLIER = 2
ARBITRARY_BOUNDARY = 30
ONE = bitarray('1')

WIN_VALUE = 1e6
ABOUT_TO_WIN = 1e4
PIECE_VALUE = 1300
PIECE_DANGER_VALUE = 10
PIECE_HIGH_DANGER_VALUE = 100
PIECE_ATTACK_VALUE = 5000
PIECE_PROTECTION_VALUE = 65
PIECE_ROW_CONNECTION_VALUE = 35
PIECE_COL_CONNECTION_VALUE = 15
PIECE_COL_HOLE_VALUE = 20
PIECE_HOME_GROUND_VALUE = 10

random.seed()

class Heuristics:
    def defensive_one(game, state):
        if state.next_to_move == PlayerName.WHITES:
            return ARBITRARY_MULTIPLIER * state.remaining_blacks() + random.random()
        elif state.next_to_move == PlayerName.BLACKS:
            return ARBITRARY_MULTIPLIER * state.remaining_whites() + random.random()

    def offensive_one(game, state):
        if state.next_to_move == PlayerName.WHITES:
            return ARBITRARY_MULTIPLIER * \
                (ARBITRARY_BOUNDARY - state.remaining_whites()) + random.random()
        else:
            return ARBITRARY_MULTIPLIER * \
                (ARBITRARY_BOUNDARY - state.remaining_blacks()) + random.random()

    """
    This heuristic takes into consideration:
    - try to protect as many cells as possible
    - delta formations are strong defenses, value them high
    - weight the cells that are protected by others
        - delta formations help with this
    - pieces in the first (W) and last (B) rows are strong defenses
    """
    def defensive_two(game, state):
        PROTECTED_CELL_VALUE = 65
        ROW_FORMATION_VALUE = 35
        DELTA_FORMATION_VALUE = 70
        UNPROTECTED_CELL_VALUE = 100
        AT_HOME_VALUE = 10
        ABOUT_TO_WIN = 1e6
        ABOUT_TO_LOSE = 1e7
        WIN = 1e9

        attacked_by_black = set()
        for black_position in state.blacks.itersearch(ONE):
            row = black_position // state.cols
            col = black_position % state.cols
            if row > 0:
                if col < state.cols - 1 and not state.blacks[ black_position - state.cols + 1 ] and \
                   not state.whites[ black_position - state.cols + 1 ]:
                    attacked_by_black.add(black_position - state.cols + 1)
                if col > 0 and not state.blacks[ black_position - state.cols - 1 ] and \
                   not state.whites[ black_position - state.cols - 1 ]:
                    attacked_by_black.add(black_position - state.cols - 1)

        protected_cells = set()
        pieces = state.whites.itersearch(ONE)
        for piece_position in pieces:
            state.value += PIECE_VALUE
            piece_row = piece_position // state.cols
            piece_col = piece_position % state.cols

            if piece_row < state.rows - 1:
                if piece_col > 0:
                    protected_cells.add((piece_row + 1) * state.cols + piece_col - 1)
                if piece_col < state.cols - 1:
                    protected_cells.add((piece_row + 1) * state.cols + piece_col + 1)

            if piece_row > 0 and piece_col > 0 and piece_col < state.cols - 1:
                if state.whites[ (piece_row - 1) * state.cols - piece_col - 1 ] and \
                   state.whites[ (piece_row - 1) * state.cols - piece_col + 1 ]:
                    state.value += DELTA_FORMATION_VALUE

            if piece_col > 0 and state.whites[ piece_position - 1 ]:
                state.value += ROW_FORMATION_VALUE

            if piece_row == state.rows - 2:
                state.value += ABOUT_TO_WIN

            if piece_row == state.rows - 1:
                state.value += WIN

            if piece_row == 0:
                state.value += AT_HOME_VALUE

        state.value += len(protected_cells) * PROTECTED_CELL_VALUE
        state.value -= len(attacked_by_black - protected_cells) * UNPROTECTED_CELL_VALUE

        attacked_by_white = set()
        for white_position in state.whites.itersearch(ONE):
            row = white_position // state.cols
            col = white_position % state.cols
            if row < state.rows - 1:
                if col < state.cols - 1 and not state.whites[ white_position + state.cols + 1 ] and \
                   not state.blacks[ white_position + state.cols + 1 ]:
                    attacked_by_white.add(white_position - state.cols + 1)
                if col > 0 and not state.whites[ white_position + state.cols - 1 ] and \
                   not state.blacks[ white_position + state.cols - 1 ]:
                    attacked_by_white.add(white_position + state.cols - 1)

        protected_cells = set()
        pieces = state.blacks.itersearch(ONE)
        for piece_position in pieces:
            piece_row = piece_position // state.cols
            piece_col = piece_position % state.cols

            if piece_row > 0:
                if piece_col > 0:
                    protected_cells.add((piece_row - 1) * state.cols + piece_col - 1)
                if piece_col < state.cols - 1:
                    protected_cells.add((piece_row - 1) * state.cols + piece_col + 1)

            if piece_row < state.rows - 1 and piece_col > 0 and piece_col < state.cols - 1:
                if state.blacks[ (piece_row + 1) * state.cols - piece_col - 1 ] and state.blacks[ (piece_row + 1) * state.cols - piece_col + 1 ]:
                    state.value -= DELTA_FORMATION_VALUE

            if piece_col > 0 and state.blacks[ piece_position - 1 ]:
                state.value -= ROW_FORMATION_VALUE

            if piece_row == 1:
                state.value -= ABOUT_TO_LOSE

            if piece_row == 0:
                state.value -= WIN

            if piece_row == state.rows - 1:
                state.value -= AT_HOME_VALUE

        state.value -= len(protected_cells) * PROTECTED_CELL_VALUE
        state.value += len(attacked_by_white - protected_cells) * UNPROTECTED_CELL_VALUE

        if state.next_to_move == PlayerName.WHITES:
            return -state.value
        return state.value


    """
    For this I'll do this:
    - give more value to positions that are closer to the goal
    - move forward as a front
    - try to protect high value pieces
    - this formation is strong as it moves forward:
        ***
         *
    """
    def offensive_two(game, state):
        INSIDE_ENEMY_TERRITORY_VALUE = 5
        LONELY_PUNISH_VALUE = 20
        ARROW_FORMATION_VALUE = 20
        NICE_CAPTURE_VALUE = 10
        ABOUT_TO_WIN = 1e3
        WIN = 1e4

        # check how good the board is for blacks since he just moved
        blacks = state.blacks.itersearch(ONE)
        for piece_position in blacks:
            piece_row = piece_position // state.cols
            piece_col = piece_position % state.cols

            if piece_row == 0:
                state.value += WIN

            if piece_row == 1:
                state.value += ABOUT_TO_WIN

            behind_position = (piece_row + 1) * state.cols

            if piece_row < state.rows - 1:
                if piece_col == 0:
                    if state.blacks[ behind_position ] and \
                       state.blacks[ behind_position + 1 ]:
                        state.value += ARROW_FORMATION_VALUE
                elif piece_col == state.cols - 1:
                    if state.blacks[ behind_position ] and \
                       state.blacks[ behind_position - 1 ]:
                        state.value += ARROW_FORMATION_VALUE
                else:
                    if state.blacks[ behind_position ] and \
                       state.blacks[ behind_position + 1 ] and \
                       state.blacks[ behind_position - 1 ]:
                        state.value += ARROW_FORMATION_VALUE

            state.value += piece_row * INSIDE_ENEMY_TERRITORY_VALUE

        for piece_position in state.whites.itersearch(ONE):
            piece_row = piece_position // state.cols
            piece_col = piece_position % state.cols

            if piece_row == state.rows - 1:
                state.value -= WIN

            if piece_row == state.rows - 2:
                state.value -= ABOUT_TO_WIN

            behind_position = (piece_row - 1) * state.cols

            if piece_row > 0:
                if piece_col == 0:
                    if state.whites[ behind_position ] and \
                       state.whites[ behind_position + 1 ]:
                        state.value += ARROW_FORMATION_VALUE
                elif piece_col == state.cols - 1:
                    if state.whites[ behind_position ] and \
                       state.whites[ behind_position - 1 ]:
                        state.value += ARROW_FORMATION_VALUE
                else:
                    if state.whites[ behind_position ] and \
                       state.whites[ behind_position + 1 ] and \
                       state.whites[ behind_position - 1 ]:
                        state.value += ARROW_FORMATION_VALUE

            state.value -= piece_row * INSIDE_ENEMY_TERRITORY_VALUE

        if state.next_to_move == PlayerName.BLACKS:
            return -state.value
        return state.value

    """
    Just for the fun of it!
    """
    def random(state):
        pass


if __name__ == '__main__':
    from breakthrough import Breakthrough
    board = Breakthrough().board_state

    board.move(13, 29)
    evaluation_value = Heuristics.defensive_one(board)
    print('[B] defensive h should be between [32, 33]: ', evaluation_value)
    evaluation_value = Heuristics.offensive_one(board)
    print('[B] offensive h should be between [28, 29]: ', evaluation_value)
    print('\n\n')

    # black moves
    board.move(-12, -28)
    evaluation_value = Heuristics.defensive_one(board)
    print('[W] defensive h should be between [32, 33]: ', evaluation_value)
    evaluation_value = Heuristics.offensive_one(board)
    print('[W] offensive h should be between [28, 29]: ', evaluation_value)
    print('\n\n')

    # white moves
    board.move(29, -28)
    evaluation_value = Heuristics.defensive_one(board)
    print('[B] defensive h should be between [30, 31]: ', evaluation_value)
    evaluation_value = Heuristics.offensive_one(board)
    print('[B] offensive h should be between [28, 29]: ', evaluation_value)
    print('\n\n')

    # black moves
    board.move(-13, -21)
    evaluation_value = Heuristics.defensive_one(board)
    print('[W] defensive h should be between [32, 33]: ', evaluation_value)
    evaluation_value = Heuristics.offensive_one(board)
    print('[W] offensive h should be between [30, 31]: ', evaluation_value)
