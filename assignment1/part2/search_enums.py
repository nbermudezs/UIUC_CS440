from enum import Enum

class SearchStrategy(Enum):
    A_STAR = 1
    BFS = 2
    DFS = 3
    GBFS = 4

class TerminalColor(Enum):
    BLUE = '\033[94m'
    RED = '\033[91m'
    DEFAULT = '\033[0m'
