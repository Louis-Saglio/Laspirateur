from with_gui import Cell


class Agent:
    def choose_cell_to_move_in(self, surroundings: dict[str, Cell]) -> Cell:
        raise NotImplementedError
