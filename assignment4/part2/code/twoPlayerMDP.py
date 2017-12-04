__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from action import PongAction
from numpy.random import uniform
from math import floor
from numpy import sign

class PongMDP:
    def __init__(self,
                 ball_x=0.5,
                 ball_y=0.5,
                 velocity_x=0.03,
                 velocity_y=0.01,
                 paddle_height=0.2,
                 paddle_step=0.04,
                 paddle_y=None,
                 paddle_y_b=None,
                 paddle_step_b=0.02,
                 id_a=None,
                 id_b=None):
        self.ball_x = ball_x
        self.ball_y = ball_y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.paddle_height = paddle_height
        self.paddle_x = 1.
        self.paddle_x_b = 0.
        self.paddle_y = paddle_y or 0.5 - self.paddle_height / 2.
        self.paddle_y_b = paddle_y_b or 0.5 - self.paddle_height / 2.
        self.paddle_step = paddle_step
        self.paddle_step_b = paddle_step_b
        self.id_a = id_a
        self.id_b = id_b

    def carry_out(self, action_a, action_b):
        # Increment ball_x by velocity_x and ball_y by velocity_y.
        self.ball_x += self.velocity_x
        self.ball_y += self.velocity_y

        # player independent
        if self.ball_y < 0:
            self.ball_y = -self.ball_y
            self.velocity_y = -self.velocity_y

        # player independent
        if self.ball_y > 1:
            self.ball_y = 2 - self.ball_y
            self.velocity_y = -self.velocity_y

        # player A paddle
        if action_a == PongAction.UP:
            self.paddle_y -= self.paddle_step
        elif action_a == PongAction.DOWN:
            self.paddle_y += self.paddle_step

        if self.paddle_y < 0:
            self.paddle_y = 0
        elif self.paddle_y > 1 - self.paddle_height:
            self.paddle_y = 1 - self.paddle_height

        # player B paddle
        if action_b == PongAction.UP:
            self.paddle_y_b -= self.paddle_step_b
        elif action_b == PongAction.DOWN:
            self.paddle_y_b += self.paddle_step_b

        if self.paddle_y_b < 0:
            self.paddle_y_b = 0
        elif self.paddle_y_b > 1 - self.paddle_height:
            self.paddle_y_b = 1 - self.paddle_height

        # ball in the air = no winner yet
        if self.ball_x < self.paddle_x and self.ball_x > self.paddle_x_b:
            return None

        U = uniform(-0.015, 0.015)
        V = uniform(-0.03, 0.03)

        # player B
        if self.ball_x < self.paddle_x_b:
            # check if hit or miss
            hit = self.ball_y > self.paddle_y_b and \
                self.ball_y < self.paddle_y_b + self.paddle_height
            if hit:
                self.ball_x = 2 * self.paddle_x_b - self.ball_x
                self.velocity_x = -self.velocity_x + U
                self.velocity_y += V

                self.velocity_x = sign(self.velocity_x) * \
                    max(abs(self.velocity_x), 0.03)

                if abs(self.velocity_x) > 1:
                    self.velocity_x = sign(self.velocity_x)

                if abs(self.velocity_y) > 1:
                    self.velocity_y = sign(self.velocity_y)
                # no winner yet
                return None
            else:
                # player B lost = player A wins
                return self.id_a

        hit = self.ball_y > self.paddle_y and \
            self.ball_y < self.paddle_y + self.paddle_height

        if hit:
            self.ball_x = 2 * self.paddle_x - self.ball_x
            self.velocity_x = -self.velocity_x + U
            self.velocity_y += V

            self.velocity_x = sign(self.velocity_x) * \
                max(abs(self.velocity_x), 0.03)

            if abs(self.velocity_x) > 1:
                self.velocity_x = sign(self.velocity_x)

            if abs(self.velocity_y) > 1:
                self.velocity_y = sign(self.velocity_y)

            # no winner yet
            return None

        # if we reached this point user A missed the ball so B wins
        return self.id_b

    def R(self):
        if self.ball_x < self.paddle_x:
            return 0
        miss = self.paddle_y > self.ball_y or \
            self.paddle_y + self.paddle_height < self.ball_y
        if miss:
            return -1
        return 1

    def as_discrete(self, grid_x=12, grid_y=12):
        # special case
        if self.ball_x > self.paddle_x:
            return (-1, -1, -1, -1, -1)

        # discretize paddle
        if self.paddle_y == 1 - self.paddle_height:
            discrete_paddle = 11.
        else:
            discrete_paddle = floor(12 * self.paddle_y / (1 - self.paddle_height))

        ball_x = int(floor(self.ball_x * grid_x))
        ball_y = int(floor(self.ball_y * grid_y))
        velocity_x = sign(self.velocity_x)
        if abs(self.velocity_y) < 0.015:
            velocity_y = 0
        else:
            velocity_y = sign(self.velocity_y)

        return (ball_x, ball_y, velocity_x, velocity_y, discrete_paddle)

    def is_terminal(self):
        return self.R() == -1

    def actions(self, state):
        return [PongAction.STILL, PongAction.DOWN, PongAction.UP]

    def __str__(self):
        return '(' + str(self.ball_x) + ',' + str(self.ball_y) + ',' +\
            str(self.velocity_x) + ',' + str(self.velocity_y) + ',' +\
            str(self.paddle_y) + ')'

if __name__ == '__main__':
    ball_x = 0.5
    ball_y = 0.5
    v_x = 0.03
    v_y = 0.01
    pong = PongMDP(ball_x=ball_x, ball_y=ball_y,
                   velocity_x=v_x, velocity_y=v_y)
    r = pong.R()
    assert(r == 0)
    assert(pong.is_terminal() == False)

    # test move paddle up and down
    pong.carry_out(PongAction.UP, PongAction.STILL)
    r = pong.R()
    assert(r == 0)
    assert(pong.ball_x == ball_x + v_x)
    assert(pong.ball_y == ball_y + v_y)
    assert(pong.paddle_y == 0.4 - 0.04)

    pong.carry_out(PongAction.DOWN, PongAction.STILL)
    assert(pong.ball_x == ball_x + 2 * v_x)
    assert(pong.ball_y == ball_y + 2 * v_y)
    assert(pong.paddle_y == 0.4)

    # test for catching the ball
    pong = PongMDP(ball_x = 1.01, paddle_y=0.1)
    r = pong.R()
    assert(r == -1)
    assert(pong.is_terminal() == True)

    pong = PongMDP(ball_x = 1.01, ball_y=0.83, paddle_y=0.6)
    r = pong.R()
    assert(r == -1)
    assert(pong.is_terminal() == True)

    pong = PongMDP(ball_x = 1.01, ball_y=0.83, paddle_y=0.7)
    r = pong.R()
    assert(r == 1)
    assert(pong.is_terminal() == False)

    # test bounces

    # top
    pong = PongMDP(ball_y=0.016, velocity_y=-0.02)
    pong.carry_out(PongAction.STILL, PongAction.STILL)
    assert(pong.ball_y == 0.004)
    assert(pong.velocity_y == 0.02)

    # bottom
    pong = PongMDP(ball_y=0.99, velocity_y=0.03)
    pong.carry_out(PongAction.STILL, PongAction.STILL)
    assert(pong.ball_y == 0.98)
    assert(pong.velocity_y == -0.03)

    pong = PongMDP(ball_x=0.4, ball_y=0.6,
                   velocity_x=0.3, velocity_y=0.01,
                   paddle_y=0.8)
    assert(pong.as_discrete() == (4, 7, 1, 0, 11))
