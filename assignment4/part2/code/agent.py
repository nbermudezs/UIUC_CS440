__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from mdp import PongMDP
from collections import defaultdict

class Agent:
    def __init__(self,
                 alpha=None,
                 gamma=None,
                 f=None):
        self.alpha = alpha
        self.gamma = gamma
        self.f = f
        self.mdp = PongMDP()
        self.Q = defaultdict(self._build_q)

    def _build_q(self):
        return defaultdict(float)

    def train(self, iterations):
        pass

    def evaluate(self, iterations):
        pass
