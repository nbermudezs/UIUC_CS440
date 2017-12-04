
from action import PongAction
from random import random

def inverse_decay(N_sa, C=5.):
    return C / (C + N_sa)

def best_action(s, Q, epsilon=0.05):
    actions = [PongAction.STILL, PongAction.DOWN, PongAction.UP]
    candidates = [(a_prime, Q[s][a_prime])
                  for a_prime in actions]
    return max(candidates, key=lambda x: x[1])

if __name__ == '__main__':
    import pickle
    from collections import defaultdict
    from gameplay import Gameplay

    with open('../models/onemillion/epoch.4000.model', 'rb') as f:
        qlAgent = pickle.load(f)

    n_games = 10000

    wins = defaultdict(int)
    for n in range(n_games):
        gameplay = Gameplay(mdp_f=best_action, player_a=qlAgent)
        winner = gameplay.play_match()
        wins[winner] += 1
    print('QLearningAgent win rate:', 1. * wins['QLearningAgent']/n_games)
