from enum import Enum
class Action(Enum):
    GO_UP = 1
    GO_DOWN = 2
    GO_LEFT = 3
    GO_RIGHT = 4
    EAT = 5

class HeuristicMethod(Enum):
    MANHATTAN = 1
    CUSTOM_1 = 2

class SearchStrategy(Enum):
    A_STAR = 1
    BFS = 2
    DFS = 3
    GBFS = 4

class TerminalColor(Enum):
    BLUE = '\033[94m'
    RED = '\033[91m'
    DEFAULT = '\033[0m'
