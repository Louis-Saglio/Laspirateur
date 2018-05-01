import random
import time
import tkinter as tk

from rooms import room1


class Direction:

    def __init__(self, height_dir, width_dir):
        self.width_dir = width_dir
        self.height_dir = height_dir


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

        self.aspirateur_cell: Cell = random.choice([cell for cell in Cell.cells.values() if cell.value.value == ' '])
        self.aspirateur_cell.move_in(Aspirateur())
        self.aspirateur_cell.show()

    def mainloop(self, n=0):
        while self.active:
            self.update()
            time.sleep(0.05)

    def destroy(self):
        self.active = False


class Aspirateur:

    def __init__(self):
        self.dir = 0

    def random_move(self, adjacents):
        for i, adjacent in enumerate(adjacents):
            if adjacent == ' ' and i == self.dir and random.randint(0, 4) != 0:
                return i
        self.dir = random.choice([n for n, adjacent in enumerate(adjacents) if adjacent == ' '])
        return self.dir


if __name__ == '__main__':
    app = RoomGui()
    app.mainloop()
