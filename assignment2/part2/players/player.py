class Player:
    def __init__(self):
        self.expanded_nodes = []
        self.time_to_move = []
        self.move_count = 0
        self.current_move_node_count = 0

    def choose_move(self, state, game):
        raise NotImplementedError
