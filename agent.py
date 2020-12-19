import random
from collections import defaultdict

from engine import DIRECTIONS, Agent, Cell


class RandomAgent(Agent):
    def choose_cell_to_move_in(self, surroundings: dict[str, Cell]) -> Cell:
        return random.choice(list(surroundings.values()))


class CleverAgent(Agent):
    def __init__(self):
        self.coordinates = 0, 0
        self.passed = defaultdict(int, {self.coordinates: 0})
        # todo : use cell as key

    def choose_cell_to_move_in(self, nearby_cells_by_direction: dict[str, Cell]) -> Cell:
        """
        surroundings : {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}
        surroundings contains only available directions
        """
        coordinates_of_nearby_cells = {}
        cp_surroundings = list(nearby_cells_by_direction.keys())
        random.shuffle(cp_surroundings)
        for next_direction in cp_surroundings:
            # compute relative coordinates of the direction
            coordinates = (
                self.coordinates[0] + DIRECTIONS[next_direction][0],
                self.coordinates[1] + DIRECTIONS[next_direction][1],
            )
            coordinates_of_nearby_cells[next_direction] = coordinates
            if coordinates not in self.passed:
                # If we are never been in this cell, let's go into
                break
        else:
            # If break statement is not raised
            next_direction = min(nearby_cells_by_direction, key=lambda x: self.passed[coordinates_of_nearby_cells[x]])
            coordinates = coordinates_of_nearby_cells[next_direction]
        self.coordinates = coordinates
        self.passed[self.coordinates] += 1
        # todo : do not assume we actually went into the selected cell
        return nearby_cells_by_direction[next_direction]
