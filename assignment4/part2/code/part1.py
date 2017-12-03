__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from action import PongAction
from random import random

def best_action(s, Q, epsilon=0.05, skip_random=False):
    actions = [PongAction.STILL, PongAction.DOWN, PongAction.UP]
    use_rand = not skip_random and random() < epsilon
    if use_rand:
        rand = int(random() * 3)
        a_prime = actions[rand]
        q_val = Q[s][a_prime]
        return a_prime, q_val

    candidates = [(a_prime, Q[s][a_prime])
                  for a_prime in actions]
    return max(candidates, key=lambda x: x[1])

def inverse_decay(N_sa, C=5.):
    return C / (C + N_sa)

if __name__ == '__main__':
    from agent import Agent
    import sys

    '''
    python part1.py --eval <path> <n_games>
    '''
    if len(sys.argv) > 2:
        import pickle
        flag = sys.argv[1]
        with open(sys.argv[2], 'rb') as f:
            agent = pickle.load(f)
            import pdb; pdb.set_trace()

        if flag == '--eval':
            agent.evaluate(int(sys.argv[3]))
        elif flag == '--resume':
            agent.train(int(sys.argv[3]))
    else:
        agent = Agent(alpha=inverse_decay,
                      f=best_action,
                      gamma=0.8)
        agent.train(10000)
        metrics = agent.evaluate(10000)
