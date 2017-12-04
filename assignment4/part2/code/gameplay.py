__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from agent import QLearningAgent
from dummyAgent import HardcodedAgent
from twoPlayerMDP import PongMDP

PLAYER_A = 'QLearningAgent'
PLAYER_B = 'HardcodedAgent'

'''
    This class holds two agents and a reference to mdp
    It takes care of playing the two-ply game between the agents.
    One agent is our QLearning agent and the other is the hardcoded one.
'''
class Gameplay:
    def __init__(self, mdp_f=None, player_a=None):
        self.mdp_f = mdp_f
        self.player_a = player_a

    def play_match(self):
        pong = PongMDP(id_a=PLAYER_A, id_b=PLAYER_B)
        player_a = self.player_a
        player_a.mdp = pong
        player_a.f = self.mdp_f
        player_b = HardcodedAgent(mdp=pong)

        winner = None

        while not winner:
            action_a = player_a.next_action()
            action_b = player_b.next_action()

            winner = pong.carry_out(action_a, action_b)
        return winner
