__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from action import PongAction
from random import random

f_count = 0
last_rand = False

def best_action(s, Q, epsilon=0.2, skip_random=False, f_count=0, last_rand=False):
    actions = [PongAction.STILL, PongAction.DOWN, PongAction.UP]
    use_rand = not skip_random and random() < epsilon
    if f_count % 2 == 0 and use_rand or f_count % 2 == 1 and not last_rand:
        rand = int(random() * 3)
        a_prime = actions[rand]
        q_val = Q[s][a_prime]
        return (a_prime, q_val), True

    candidates = [(a_prime, Q[s][a_prime])
                  for a_prime in actions]
    return max(candidates, key=lambda x: x[1]), False

def inverse_decay(N_sa, C=1.):
    return C / (C + N_sa)

if __name__ == '__main__':
    from agent import Agent
    from time import time
    import sys

    start = time()

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
                      gamma=0.9)
        agent.train(100000)
        metrics = agent.evaluate(10000)
    print('Finished in ', time() - start, 's')
