import random
import time
import tkinter as tk

from rooms import room1


DIRECTIONS = {
    'UP': (-1, 0),
    'DOWN': (+1, 0),
    'LEFT': (0, -1),
    'RIGHT': (0, +1)
}


class Value:
    colors = {'M': 'blue', ' ': 'yellow', 'aspirateur': 'red', 'passed': 'green'}

    def __init__(self, value):
        self.value = value

    def __hash__(self):
        return hash(self.value)


class Cell:
    cells = {}

    def __init__(self, room: "RoomGui", value: Value, coordinates):
        self.room = room
        self.value = value
        self.contains = set()
        self.coordinates = coordinates
        self.passed = False
        Cell.cells[self.coordinates] = self

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

    def get_surroundings(self):
        surroundings = {}
        for name, direction in DIRECTIONS.items():
            surrounding: Cell = Cell.cells[(self.coordinates[0] + direction[0], self.coordinates[1] + direction[1])]
            if surrounding.value.value == ' ':
                surroundings[name] = surrounding
        return surroundings

    def show(self):
        if self.contains_aspirateur():
            color = Value.colors['aspirateur']
        elif self.passed:
            color = Value.colors['passed']
        else:
            color = Value.colors[self.value.value]
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

        for i, row in enumerate(self.data):
            for j, cell in enumerate(row):
                Cell(self, Value(cell), (i, j)).show()

        self.aspirateur = Aspirateur()
        self.aspirateur_cell: Cell = random.choice([cell for cell in Cell.cells.values() if cell.value.value == ' '])
        self.aspirateur_cell.move_in(self.aspirateur)
        self.aspirateur_cell.show()

    def mainloop(self, n=0):
        while self.active:
            self.update()
            self.aspirateur_cell.move_from(self.aspirateur)
            self.aspirateur_cell.show()
            self.aspirateur_cell = self.aspirateur.random_move(self.aspirateur_cell.get_surroundings())
            self.aspirateur_cell.move_in(self.aspirateur)
            self.aspirateur_cell.show()
            time.sleep(0.05)

    def destroy(self):
        self.active = False


class Aspirateur:

    def random_move(self, surroundings: dict) -> Cell:
        return random.choice(list(surroundings.values()))


if __name__ == '__main__':
    app = RoomGui()
    app.mainloop()
