__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from breakthrough import Breakthrough, Breakthrough3WorkersToBase, BreakthroughBoard, Util
from players import alpha_beta_player, minimax_player
from heuristics import Heuristics

def matrix_to_board(matrix):
    from bitarray import bitarray
    whites = ''
    blacks = ''
    for row in matrix:
        for col in row:
            whites += ('1' if col == 'W' else '0')
            blacks += ('1' if col == 'B' else '0')
    board = BreakthroughBoard(len(matrix), len(matrix[ 0 ]))
    board.whites = bitarray(whites)
    board.blacks = bitarray(blacks)
    return board

if __name__ == '__main__':
    breakthrough = Breakthrough3WorkersToBase(10, 5)

    # TODO: remember to repeat games a lot of times to get statistics!
    playerA = alpha_beta_player.AlphaBetaPlayer(heuristic = Heuristics.offensive_one)
    # playerB = minimax_player.MinimaxPlayer(heuristic = Heuristics.defensive_one)
    playerB = alpha_beta_player.AlphaBetaPlayer(heuristic = Heuristics.defensive_one)
    breakthrough.play_game(playerA, playerB)
    print('White stats', playerA)
    print('Black stats', playerB)

    # matrix = [[ ' ', ' ', 'W', 'W', 'W', 'W', ' ', 'W' ],
    #           [ 'W', ' ', ' ', 'W', ' ', 'W', ' ', 'W' ],
    #           [ 'B', 'W', 'W', ' ', 'W', ' ', 'W', 'W' ],
    #           [ ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' ],
    #           [ ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' ],
    #           [ ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' ],
    #           [ ' ', ' ', 'B', 'B', 'B', 'B', 'B', 'B' ],
    #           [ 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B' ]]
    # board = matrix_to_board(matrix)
    # Util.print_board(board, board.rows, board.cols)
    # breakthrough.board_state = board
    # breakthrough.play_game(playerA, playerB)
