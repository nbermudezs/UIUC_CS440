class Node:
    def __init__(self, position, cell_type):
        self.path_cost = 0
        self.parent = None
        self.position = position
        self.cell_type = cell_type
        self.child = {}
        self.child_count = 0

    def append(self, child):
        child.parent = self
        self.child[ self.child_count ] = child
        self.child_count += 1
