import random
import time
import tkinter as tk

from rooms import room1


class Direction:

    def __init__(self, height_dir, width_dir):
        self.width_dir = width_dir
        self.height_dir = height_dir


class Cell:

    def __init__(self, room: "RoomGui", value):
        self.room = room
        self.value = value
        self.contains = set()

    def __contains__(self, item):
        return item in self.contains


class RoomGui(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('Laspirateur')
        self.data = room1
        self.height = len(self.data)
        self.width = len(self.data[0])
        self.aspi_coord = 1, 2
        self.passed = {self.aspi_coord}
        self.aspi = Aspirateur()
        self.active = True
        for i, row in enumerate(self.data):
            for j, cell in enumerate(row):
                if cell == 'M':
                    color = 'blue'
                else:
                    color = 'yellow'
                tk.Frame(self, height=20, width=20, background=color).grid(row=i, column=j)
        tk.Frame(self, height=20, width=20, background='red').grid(row=self.aspi_coord[0], column=self.aspi_coord[1])

    def move_aspi(self, x, y):
        tk.Frame(self, height=20, width=20, background='green').grid(row=self.aspi_coord[0], column=self.aspi_coord[1])
        self.aspi_coord = x, y
        self.passed.add(self.aspi_coord)
        tk.Frame(self, height=20, width=20, background='red').grid(row=self.aspi_coord[0], column=self.aspi_coord[1])

    def mainloop(self, n=0):
        while self.active:
            self.update()
            self.move_aspi_by_dir_code(self.aspi.random_move(self.get_aspi_adjacent()))
            time.sleep(0.05)

    def destroy(self):
        self.active = False

    def get_aspi_adjacent(self):
        return (
            self.data[self.aspi_coord[0] - 1][self.aspi_coord[1]],
            self.data[self.aspi_coord[0] + 1][self.aspi_coord[1]],
            self.data[self.aspi_coord[0]][self.aspi_coord[1] - 1],
            self.data[self.aspi_coord[0]][self.aspi_coord[1] + 1]
        )

    def move_aspi_by_dir_code(self, dir_code):
        if dir_code == 0:
            self.move_aspi(self.aspi_coord[0] - 1, self.aspi_coord[1])
        elif dir_code == 1:
            self.move_aspi(self.aspi_coord[0] + 1, self.aspi_coord[1])
        elif dir_code == 2:
            self.move_aspi(self.aspi_coord[0], self.aspi_coord[1] - 1)
        elif dir_code == 3:
            self.move_aspi(self.aspi_coord[0], self.aspi_coord[1] + 1)


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
