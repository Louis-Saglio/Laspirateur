import random
from collections import defaultdict

from engine import DIRECTIONS, Agent, DIRECTION

DIRECTIONS_TUPLE = tuple[DIRECTION, ...]


class RandomAgent(Agent):
    def choose_cell_to_move_in(self, available_directions: DIRECTIONS_TUPLE) -> DIRECTION:
        return random.choice(available_directions)


class CleverAgent(Agent):
    def __init__(self):
        self.coordinates = 0, 0
        self.passed = defaultdict(int, {self.coordinates: 0})

    def choose_cell_to_move_in(self, available_directions: DIRECTIONS_TUPLE) -> DIRECTION:
        """
        surroundings : {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}
        surroundings contains only available directions
        """
        coordinates_of_nearby_cells_by_direction = {}
        available_directions = list(available_directions)
        random.shuffle(available_directions)
        for next_direction in available_directions:
            # compute relative coordinates of the direction
            coordinates = (
                self.coordinates[0] + DIRECTIONS[next_direction][0],
                self.coordinates[1] + DIRECTIONS[next_direction][1],
            )
            coordinates_of_nearby_cells_by_direction[next_direction] = coordinates
            if coordinates not in self.passed:
                # If we are never been in this cell, let's go into
                break
        else:
            # If break statement is not raised
            next_direction = min(
                available_directions,
                key=lambda direction: self.passed[coordinates_of_nearby_cells_by_direction[direction]],
            )
            coordinates = coordinates_of_nearby_cells_by_direction[next_direction]
        self.coordinates = coordinates
        self.passed[self.coordinates] += 1
        return next_direction


class SarsaAgent(Agent):
    def __init__(self):
        # self.q_table: dict[tuple[DIRECTIONS_TUPLE, DIRECTION], float] = defaultdict(int)
        self.q_table: dict[DIRECTIONS_TUPLE, dict[DIRECTION, float]] = defaultdict(lambda: defaultdict(float))
        self.previous_perception: DIRECTIONS_TUPLE = None
        self.previous_action: DIRECTION = None
        self.previous_reward = 0
        self.learning_rate = 0.5
        self.discount_factor = 0.9
        self.coordinates = 0, 0
        self.passed = defaultdict(int, {self.coordinates: 0})

    def choose_cell_to_move_in(self, available_directions: DIRECTIONS_TUPLE) -> DIRECTION:
        self.q_table[self.previous_perception][self.previous_action] += self.learning_rate * (
            self.previous_reward
            + self.discount_factor * self.q_table[available_directions][None]
            - self.q_table[self.previous_perception][self.previous_action]
        )
        self
