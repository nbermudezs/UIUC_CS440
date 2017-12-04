__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from action import PongAction

class HardcodedAgent:
    def __init__(self, mdp=None):
        self.mdp = mdp

    def next_action(self):
        ball_y = self.mdp.ball_y
        mid = self.mdp.paddle_y_b + self.mdp.paddle_height / 2.
        if abs(mid - ball_y) < 0.05:
            return PongAction.STILL
        if mid < ball_y:
            return PongAction.DOWN

        return PongAction.UP

    def play_turn(self):
        a = self.best_action()
        r = self.carry_out(a)
        return r == -1
