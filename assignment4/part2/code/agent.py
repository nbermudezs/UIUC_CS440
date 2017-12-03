__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from mdp import PongMDP
from collections import defaultdict

import pickle

class Agent:
    def __init__(self,
                 alpha=None,
                 gamma=None,
                 f=None):
        self.alpha = alpha
        self.gamma = gamma
        self.f = f
        self.Q = defaultdict(self._build_q)

    def _build_q(self):
        return defaultdict(float)

    def train(self, iterations):
        for epoch in range(iterations):
            metrics = self.single_run()

            if epoch % 1000 == 0:
                self.save(epoch)

    def evaluate(self, iterations):
        for epoch in range(iterations):
            metrics = self.single_run()

    '''
        Run a single game until agent looses
    '''
    def single_run(self):
        total_hits = 0
        total_moves = 0
        self.mdp = PongMDP()

        return (total_moves, total_hits)

    '''
        Dump into pickled file
    '''
    def save(self, epoch):
        path = '../models/run' + str(epoch) + '.model'
        print('Saving model to', path)
        with open(path, 'wb') as f:
            pickle.dump(self, f)
