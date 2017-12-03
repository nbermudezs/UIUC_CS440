__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

if __name__ == '__main__':
    from agent import Agent

    agent = Agent()
    agent.train(100000)
    metrics = agent.evaluate(10000)
