import functools
import math

from bitarray import bitarray
from enum import Enum
from munkres import Munkres

STORED_BOX = 'B'
UNSTORED_BOX = 'b'
STORAGE_LOCATION = '.'
FREE_PATH = ' '
WALL = '%'
START_POINT = 'P'

# import pdb

class Action(Enum):
    GO_UP = 1
    GO_DOWN = 2
    GO_LEFT = 3
    GO_RIGHT = 4

ONE = bitarray('1')
ZERO = bitarray('0')

munkres_instance = Munkres()
munkres_results = {}

class Util:
    @staticmethod
    def manhattan_distance(x, y):
        return math.fabs(x[ 0 ] - y[ 0 ]) + math.fabs(x[ 1 ] - y[ 1 ])

    @staticmethod
    def unidimensional_manhattan_distance(a, b, column_count):
        return math.fabs(a - b) // count + math.fabs(a - b) % count

"""
I'm basing my implementation in the algorithm described in
http://www.hungarianalgorithm.com/examplehungarianalgorithm.php
"""
class HungarianMethod:
    def __init__(self, position, box_state, storage_locations, problem):
        empty_storage_locations = ~ box_state & storage_locations
        misplaced_boxes = ~ storage_locations & box_state
        matrix = []

        box_indexes = misplaced_boxes.search(ONE)
        agent_position = (position // problem.column_count, position % problem.column_count)

        self.distance_to_agent = float('inf')
        self.cache_key = empty_storage_locations.to01() + misplaced_boxes.to01()

        if self.cache_key in munkres_results:
            for box_index in box_indexes:
                box = (box_index // problem.column_count, box_index % problem.column_count)
                self.distance_to_agent = min(self.distance_to_agent, Util.manhattan_distance(agent_position, box))
            return

        storage_indexes = empty_storage_locations.search(ONE)

        for row, storage_index in enumerate(storage_indexes):
            a = (storage_index // problem.column_count, storage_index % problem.column_count)
            matrix.append([])
            for col, box_index in enumerate(box_indexes):
                b = (box_index // problem.column_count, box_index % problem.column_count)
                matrix[ row ].append(Util.manhattan_distance(a, b))
                self.distance_to_agent = min(self.distance_to_agent, Util.manhattan_distance(agent_position, b))

        self.distance_matrix = matrix
        #
        # print(box_indexes)
        # print(storage_indexes)
        # print('Distance to agent', self.distance_to_agent)
        # print('Hungarian matrix', self.distance_matrix)

    def solve(self):
        if self.cache_key not in munkres_results:
            matrix = self.distance_matrix
            indexes = munkres_instance.compute(matrix)
            # print('INDEXES!', indexes, matrix)
            result = sum([ matrix[ row ][ col ] for row, col in indexes ])
            munkres_results[ self.cache_key ] = result
        return munkres_results[ self.cache_key ] + self.distance_to_agent

class Heuristic:
    # find a way to cache these results. lru_cache doesn't work because bitarray
    # is not hashable
    @staticmethod
    def hungarian_method(position, box_state, storage_locations, problem):
        return HungarianMethod(position, box_state, storage_locations, problem).solve()

    @staticmethod
    def suboptimal_search(position, box_state, storage_locations, problem):
        box_indexes = box_state.search(ONE)
        storage_indexes = storage_locations.search(ONE)

        total_weight = 0
        start_box = None
        start_box_index = 0
        for box_index in box_indexes:
            dist_to_storage = float('inf')
            for storage_index in storage_indexes:
                box = (box_index // problem.column_count, box_index % problem.column_count)
                s = (storage_index // problem.column_count, storage_index % problem.column_count)
                d = Util.manhattan_distance(s, box)
                if d < dist_to_storage:
                    dist_to_storage = d
                    start_box = box
                    start_box_index = box_index
            total_weight += dist_to_storage

        prev_box = start_box
        prev_box_index = start_box_index
        while len(box_indexes) > 1:
            box_indexes.remove(prev_box_index)
            dist_to_box = float('inf')
            temp_box = None
            for box_index in box_indexes:
                box = (box_index // problem.column_count, box_index % problem.column_count)
                d = Util.manhattan_distance(prev_box, box)
                if dist_to_box > d:
                    temp_box = box
                    prev_box_index = box_index
                    dist_to_box = d

            prev_box = temp_box
            total_weight += dist_to_box

        return total_weight*3

class SokobanProblemState:
    def __init__(self, position, box_state, problem):
        if box_state.count(1) == 1:
            pdb.set_trace()
        """
        Bitmap of the form '0001000010'
        where the length is the number of cells in the maze.
        All 0 by default, except the positions where the boxes are currently in.
        The number of 1's in the bitmap doesn't change over time
        """
        self.box_state = box_state

        """
        Position number in the linearized maze.
        If the position in the maze was 1,2 and the maze is 5x6 this number would be
        1 * 6 + 2 = 8
        """
        self.position = position

        """
        Reference to the problem
        """
        self.problem = problem

        """
        Priority for tiebreaking
        """
        self.priority = 0

    # DONE
    def __eq__(self, other):
        return self.position == other.position and self.box_state == other.box_state

    # DONE
    def __ne__(self, other):
        return self.position != other.position or self.box_state != other.box_state

    # DONE
    def __lt__(self, other):
        placed = (self.problem.storage_locations & self.box_state).count(1)
        other_placed = (other.problem.storage_locations & other.box_state).count(1)
        return placed > other_placed

    # DONE
    def __hash__(self):
        return hash((self.box_state.to01(), self.position))

    # DONE
    def __repr__(self):
        return repr(self.position) + ':' + self.box_state.to01()

    # DONE
    def __str__(self):
        return '[ pos = ' + str(self.position) + '\tboxes = ' + self.box_state.to01() + ' ]'

    # DONE
    def up(self):
        new_position = self.position - self.problem.column_count
        next_position = new_position - self.problem.column_count
        if self.box_state[ new_position ] and next_position >= 0:
            new_box_state = bitarray(self.box_state)
            new_box_state[ next_position ] = self.box_state[ new_position ]
            new_box_state[ new_position ] = 0
            return SokobanProblemState(new_position, new_box_state, self.problem)
        else:
            return SokobanProblemState(new_position, self.box_state, self.problem)

    # DONE
    def down(self):
        new_position = self.position + self.problem.column_count
        next_position = new_position + self.problem.column_count
        if self.box_state[ new_position ] and next_position < self.problem.cell_count:
            new_box_state = bitarray(self.box_state)
            new_box_state[ next_position ] = self.box_state[ new_position ]
            new_box_state[ new_position ] = 0
            return SokobanProblemState(new_position, new_box_state, self.problem)
        else:
            return SokobanProblemState(new_position, self.box_state, self.problem)

    # DONE
    def right(self):
        new_position = self.position + 1
        next_position = new_position + 1
        if self.box_state[ new_position ] and self.position % self.problem.column_count + 2 < self.problem.column_count:
            new_box_state = bitarray(self.box_state)
            new_box_state[ next_position ] = self.box_state[ new_position ]
            new_box_state[ new_position ] = 0
            return SokobanProblemState(new_position, new_box_state, self.problem)
        else:
            return SokobanProblemState(new_position, self.box_state, self.problem)

    # DONE
    def left(self):
        new_position = self.position - 1
        next_position = new_position - 1
        if self.box_state[ new_position ] and self.position % self.problem.column_count - 2 >= 0:
            new_box_state = bitarray(self.box_state)
            new_box_state[ next_position ] = self.box_state[ new_position ]
            new_box_state[ new_position ] = 0
            return SokobanProblemState(new_position, new_box_state, self.problem)
        else:
            return SokobanProblemState(new_position, self.box_state, self.problem)

class SokobanProblem():
    # DONE
    def __init__(self):
        """
        Store the bidimensional representation of the maze to print it when done
        """
        self.maze = []
        self.storage_count = 0

        """
        Mapping between the action name and the function that will perform the action
        This way I don't have to run if/elif every time.
        """
        self.action_map = {}
        self.action_map[ Action.GO_UP ] = SokobanProblemState.up
        self.action_map[ Action.GO_DOWN ] = SokobanProblemState.down
        self.action_map[ Action.GO_LEFT ] = SokobanProblemState.left
        self.action_map[ Action.GO_RIGHT ] = SokobanProblemState.right

        self.row_count = 0
        self.column_count = 0
        self.cell_count = 0

        """
        Bitmap of the size of the maze.
        All bits are 0 except the ones where there is a wall.
        It doesn't change over time.
        """
        self.walls = None

        """
        Bitmap to hold the position of the storage locations
        """
        self.storage_locations = None

        """
        Initial state
        """
        self.initial_state = None

    def load(self, filepath):
        file_object = open(filepath, 'r')
        text = file_object.read()

        # last line is an empty newline so we remove it.
        lines = text.split('\n')[:-1]
        self.row_count = len(lines)
        self.column_count = len(lines[ 0 ])
        self.cell_count = self.row_count * self.column_count
        self.maze = [ [char for char in line] for line in lines ]

        initial_box_positions = bitarray(self.row_count * self.column_count)
        initial_box_positions.setall(0)

        self.walls = bitarray(self.row_count * self.column_count)
        self.walls.setall(0)

        self.storage_locations = bitarray(self.row_count * self.column_count)
        self.storage_locations.setall(0)

        start_point = None
        for i, row in enumerate(lines):
            for j, char in enumerate(row):
                if char == WALL:
                    self.walls[ i * self.column_count + j ] = 1
                elif char == STORED_BOX or char == UNSTORED_BOX:
                    initial_box_positions[ i * self.column_count + j ] = 1
                    if char == STORED_BOX:
                        self.storage_locations[ i * self.column_count + j ] = 1
                elif char == STORAGE_LOCATION:
                    self.storage_locations[ i * self.column_count + j ] = 1
                elif char == START_POINT:
                    start_point = i * self.column_count + j

        self.storage_count = self.storage_locations.count(1)
        self.initial_state = SokobanProblemState(start_point, initial_box_positions, self)
        # print('start position', start_point, self.column_count, self.row_count)
        # print('boxes:\t\t\t', initial_box_positions.to01())
        # print('storage:\t\t', self.storage_locations.to01())
        # print('walls:\t\t\t', self.walls.to01())

    # DONE
    @functools.lru_cache(maxsize=8196)
    def actions(self, state):
        legal_actions = []
        index = state.position
        walls = self.walls
        obstacles = state.box_state | walls

        """
        The meaning of the following code is:
        you can go in a given direction if
        - there is no obstacle in the target position or
        - there is a box in the target position and the next position in the same
            direction doesn't have any obstacle
        """
        can_go_up = not obstacles[ index - self.column_count ] or \
            state.box_state[ index - self.column_count ] and \
            index - self.column_count * 2 >= 0 and \
            not obstacles[ index - self.column_count * 2 ]
        if can_go_up:
            legal_actions.append(Action.GO_UP)

        can_go_down = not obstacles[ index + self.column_count ] or \
            state.box_state[ index + self.column_count ] and \
            index + self.column_count * 2 < self.cell_count and \
            not obstacles[ index + self.column_count * 2 ]
        if can_go_down:
            legal_actions.append(Action.GO_DOWN)

        can_go_right = not obstacles[ index + 1 ] or \
            state.box_state[ index + 1 ] and \
            index % self.column_count + 2 < self.column_count and \
            not obstacles[ index + 2 ]
        if can_go_right:
            legal_actions.append(Action.GO_RIGHT)

        can_go_left = not obstacles[ index - 1 ] or \
            state.box_state[ index - 1 ] and \
            index % self.column_count - 2 >= 0 and \
            not obstacles[ index - 2 ]
        if can_go_left:
            legal_actions.append(Action.GO_LEFT)

        return legal_actions

    # DONE
    @functools.lru_cache(maxsize=8196)
    def goal_test(self, state):
        return state.problem.storage_locations & state.box_state == state.problem.storage_locations

    # DONE
    def step_cost(self, state, action):
        return 1

    # DONE.
    @functools.lru_cache(maxsize=8196)
    def result(self, state, action):
        return self.action_map[ action ](state)

    @functools.lru_cache(maxsize=8196)
    def estimated_cost(self, state):
        empty_storage_locations = ~ state.box_state & self.storage_locations
        if empty_storage_locations.count() == 0:
            return 0
        return Heuristic.hungarian_method(state.position, state.box_state, self.storage_locations, self)

    # DONE
    def print_solution_path(self, node):
        pass

if __name__ == '__main__':
    problem = SokobanProblem()
    problem.load('./input/input1.txt')
    legal_actions = problem.actions(problem.initial_state)
    assert len(legal_actions) == 2
    assert Action.GO_UP in legal_actions
    assert Action.GO_DOWN in legal_actions

    print(problem.initial_state)
    next_step = problem.initial_state.up()
    print(next_step)
    legal_actions = problem.actions(next_step)
    assert len(legal_actions) == 3
    assert Action.GO_UP in legal_actions
    assert Action.GO_DOWN in legal_actions
    assert Action.GO_RIGHT in legal_actions

    next_step = next_step.right()
    print(next_step)
    legal_actions = problem.actions(next_step)
    assert len(legal_actions) == 2
    assert Action.GO_LEFT in legal_actions
    assert Action.GO_RIGHT in legal_actions

    next_step = next_step.right()
    print(next_step)
    legal_actions = problem.actions(next_step)
    assert len(legal_actions) == 2
    assert Action.GO_LEFT in legal_actions
    assert Action.GO_UP in legal_actions

    next_step = next_step.up()
    print(next_step)
    legal_actions = problem.actions(next_step)
    assert len(legal_actions) == 3
    assert Action.GO_UP in legal_actions
    assert Action.GO_DOWN in legal_actions
    assert Action.GO_RIGHT in legal_actions

    next_step = next_step.up()
    print(next_step)
    legal_actions = problem.actions(next_step)
    assert len(legal_actions) == 3
    assert Action.GO_LEFT in legal_actions
    assert Action.GO_DOWN in legal_actions
    assert Action.GO_RIGHT in legal_actions

    next_step = next_step.left()
    print(next_step)
    legal_actions = problem.actions(next_step)
    assert len(legal_actions) == 2
    assert Action.GO_LEFT in legal_actions
    assert Action.GO_RIGHT in legal_actions

    next_step = next_step.left()
    print(next_step)
    legal_actions = problem.actions(next_step)
    assert len(legal_actions) == 2
    assert Action.GO_DOWN in legal_actions
    assert Action.GO_RIGHT in legal_actions

    next_step = next_step.down()
    print(next_step)
    legal_actions = problem.actions(next_step)
    assert len(legal_actions) == 2
    assert Action.GO_UP in legal_actions
    assert Action.GO_DOWN in legal_actions

    assert repr(next_step) == '13:000000000000000000010010000000000000000000'

    assert problem.goal_test(next_step)

    print('Goal reached?', problem.goal_test(next_step))
    print('___________________________________________')

    print('State comparison tests')
    print('last state < initial state:', next_step < problem.initial_state)
    assert next_step < problem.initial_state

    print('last state != initial state', next_step != problem.initial_state)
    assert next_step != problem.initial_state

    clone = SokobanProblemState(next_step.position, bitarray(next_step.box_state), problem)
    print('last state == clone of last state', next_step == clone)
    assert next_step == clone
