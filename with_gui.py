import random
import time
import tkinter as tk
from typing import Dict

from rooms import room1, room2

DIRECTIONS = {
    'UP': (-1, 0),
    'DOWN': (+1, 0),
    'LEFT': (0, -1),
    'RIGHT': (0, +1)
}

COLORS = {'M': 'blue', ' ': 'yellow', 'aspirateur': 'red', 'passed': 'green'}


class Cell:

    def __init__(self, room: "RoomGui", value, coordinates):
        self.room = room
        self.value = value
        self.contains = set()
        self.coordinates = coordinates
        self.passed = False

    def move_in(self, pawn):
        self.contains.add(pawn)
        if isinstance(pawn, Aspirateur):
            self.passed = True
        self.show()

    def move_from(self, pawn):
        self.contains.remove(pawn)
        self.show()

    def contains_aspirateur(self):
        for item in self.contains:
            if isinstance(item, Aspirateur):
                return True
        return False

    def show(self):
        if self.contains_aspirateur():
            color = COLORS['aspirateur']
        elif self.passed:
            color = COLORS['passed']
        else:
            color = COLORS[self.value]
        tk.Frame(
            self.room,
            height=self.room.cell_height,
            width=self.room.cell_width,
            background=color
        ).grid(row=self.coordinates[0], column=self.coordinates[1])

    def __hash__(self):
        return hash(self.coordinates)


class RoomGui(tk.Tk):

    def __init__(self, aspirateur_class: type, room: str):
        super().__init__()
        self.loop_number = 0
        self.title('Laspirateur')
        self.active = True

        self.data = room
        self.cell_height = 20
        self.cell_width = 20

        self.cells = {}
        for i, row in enumerate(self.data):
            for j, cell in enumerate(row):
                self.cells[i, j] = Cell(self, cell, (i, j))
                self.cells[i, j].show()

        self.aspirateur: Aspirateur = aspirateur_class()
        # self.aspirateur_cell: Cell = random.choice([cell for cell in self.cells.values() if cell.value == ' '])
        self.aspirateur_cell: Cell = self.cells[(5, 5)]
        self.aspirateur_cell.move_in(self.aspirateur)
        self.aspirateur_cell.show()

    def get_surroundings(self, cell: Cell):
        surroundings = {}
        for name, direction in DIRECTIONS.items():
            surrounding: Cell = self.cells[(cell.coordinates[0] + direction[0], cell.coordinates[1] + direction[1])]
            if surrounding.value == ' ':
                surroundings[name] = surrounding
        return surroundings

    def mainloop(self, n=0):
        while self.active:
            self.loop_number += 1
            self.update()
            self.aspirateur_cell.move_from(self.aspirateur)
            self.aspirateur_cell = self.aspirateur.move(self.get_surroundings(self.aspirateur_cell))
            self.aspirateur_cell.move_in(self.aspirateur)
            time.sleep(0.05)

    def destroy(self):
        print(self.loop_number)
        self.active = False


class Aspirateur:

    def move(self, surroundings: Dict[str, Cell]) -> Cell:
        raise NotImplementedError


class AspirateurRandom(Aspirateur):

    def __init__(self):
        self.last_cells = None, None

    def move(self, surroundings: Dict[str, Cell]) -> Cell:
        return random.choice(list(surroundings.values()))


class CleverAspirateur(Aspirateur):

    def __init__(self):
        self.coordinates = 0, 0
        self.passed = {self.coordinates: 0}

    def move(self, surroundings: Dict[str, Cell]) -> Cell:
        """
        surroundings : {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}
        surroundings contains only available directions
        """
        buffer = {}
        for next_direction in surroundings:
            # compute relative coordinates of the direction
            coordinates = (
                self.coordinates[0] + DIRECTIONS[next_direction][0],
                self.coordinates[1] + DIRECTIONS[next_direction][1]
            )
            buffer[next_direction] = coordinates
            if coordinates not in self.passed:
                # If we are never been in this cell, let's go into
                break
        else:
            # If break statement is not raised
            next_direction = min(surroundings, key=lambda x: self.passed[buffer[x]])
            coordinates = buffer[next_direction]
        self.coordinates = coordinates
        if self.coordinates in self.passed:
            self.passed[self.coordinates] += 1
        else:
            self.passed[self.coordinates] = 1
        return surroundings[next_direction]


if __name__ == '__main__':
    app = RoomGui(CleverAspirateur, room3)
    app.mainloop()
