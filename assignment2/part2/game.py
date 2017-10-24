__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

class Game:
    def actions(self, state):
        raise NotImplementedError

    def result(self, state, move):
        raise NotImplementedError

    def utility(self, state, player):
        raise NotImplementedError

    def terminal_test(self, state):
        raise NotImplementedError

    def player_to_move(self, state):
        raise NotImplementedError

    def display(self):
        raise NotImplementedError

    def __repr__(self):
        return ''

    def play_game(self, *players):
        raise NotImplementedError
