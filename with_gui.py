import random
import tkinter as tk

from rooms import room1

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

    def move_from(self, pawn):
        self.contains.remove(pawn)

    def __contains__(self, item):
        return item in self.contains

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

    def __init__(self):
        super().__init__()
        self.title('Laspirateur')
        self.active = True

        self.data = room1
        self.cell_height = 20
        self.cell_width = 20

        self.cells = {}
        for i, row in enumerate(self.data):
            for j, cell in enumerate(row):
                self.cells[i, j] = Cell(self, cell, (i, j))
                self.cells[i, j].show()

        self.aspirateur = Aspirateur()
        self.aspirateur_cell: Cell = random.choice([cell for cell in self.cells.values() if cell.value == ' '])
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
            self.update()
            self.aspirateur_cell.move_from(self.aspirateur)
            self.aspirateur_cell.show()
            self.aspirateur_cell = self.aspirateur.random_move(self.get_surroundings(self.aspirateur_cell))
            self.aspirateur_cell.move_in(self.aspirateur)
            self.aspirateur_cell.show()

    def destroy(self):
        self.active = False


class Aspirateur:

    def __init__(self):
        self.last_cell = None
        self.move = self.random_move

    def random_move(self, surroundings: dict) -> Cell:
        surroundings = list(surroundings.values())
        next_cell = random.choice(surroundings)
        while len(surroundings) > 1 and next_cell is self.last_cell:
            next_cell = random.choice(surroundings)
        return next_cell


if __name__ == '__main__':
    app = RoomGui()
    app.mainloop()
