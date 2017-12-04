__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from mdp import PongMDP
from collections import defaultdict
from util import Util

import pickle
import numpy as np

class Agent:
    def __init__(self,
                 alpha=None,
                 gamma=None,
                 f=None,
                 mdp=None):
        self.alpha = alpha
        self.gamma = gamma
        self.best_action = f
        self.mdp = mdp
        self.Q = defaultdict(self._build_q)
        self.N = defaultdict(self._build_q)

    def _build_q(self):
        return defaultdict(float)

    def train(self, iterations):
        all_hits = []
        means = []
        for epoch in range(iterations):
            self.mdp = PongMDP()
            metrics = self.single_run()
            all_hits.append(metrics[1])

            if epoch % 1000 == 0:
                self.save(epoch)
                means.append(np.mean(all_hits))
                print('Train: mean=', np.mean(all_hits), 'std=', np.std(all_hits),
                      'max=', max(all_hits), 'min=', min(all_hits))
        Util.plot_training_curve(means)

    def evaluate(self, iterations):
        hits = []
        for epoch in range(iterations):
            self.mdp = PongMDP()
            metrics = self.single_run(skip_random=True)
            hits.append(metrics[1])
        print('Eval: mean=', np.mean(hits), 'std=', np.std(hits),
              'max=', max(hits), 'min=', min(hits))

    '''
        Run a single game until agent looses
    '''
    def single_run(self, skip_random=False):
        total_hits = 0
        total_moves = 0

        while True:
            s = self.mdp.as_discrete()
            a, value = self.best_action(s, self.Q, skip_random=skip_random)
            r = self.mdp.carry_out(a)
            s_prime = self.mdp.as_discrete()
            _, best = self.best_action(s_prime, self.Q, skip_random=skip_random)

            self.N[s][a] += 1
            self.Q[s][a] = value + self.alpha(self.N[s][a]) * (r + self.gamma * best - value)

            total_moves += 1
            if r == -1:
                # print('game over', total_hits)
                break
            elif r == 1:
                total_hits += 1
        return (total_moves, total_hits)

    def next_action(self):
        s = self.mdp.as_discrete()
        action, _ = self.best_action(s, self.Q)
        return action

    '''
        Dump into pickled file
    '''
    def save(self, epoch):
        path = '../models/run2/epoch.' + str(epoch) + '.model'
        print('Saving model to', path)
        with open(path, 'wb') as f:
            pickle.dump(self, f)

QLearningAgent = Agent
