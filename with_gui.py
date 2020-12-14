from __future__ import annotations

import random
import time
import tkinter as tk
from typing import Dict, Type, List, Tuple

DIRECTIONS = {"UP": (-1, 0), "DOWN": (+1, 0), "LEFT": (0, -1), "RIGHT": (0, +1)}

COLORS = {"M": "blue", " ": "yellow", "aspirateur": "red", "passed": "green"}


class Cell:
    def __init__(self, room: RoomGui, value: str, coordinates: Tuple[int, int]):
        self.room = room
        self.value = value
        self.content = set()
        self.coordinates = coordinates
        self.has_been_visited = False
        self.frame = None

    def move_in(self, pawn: object) -> None:
        self.content.add(pawn)
        self.has_been_visited = True
        self.show()

    def move_from(self, pawn: object) -> None:
        self.content.remove(pawn)
        self.show()

    def contains_aspirateur(self) -> bool:
        for item in self.content:
            if isinstance(item, Aspirateur):
                return True
        return False

    def show(self) -> None:
        if self.contains_aspirateur():
            color = COLORS["aspirateur"]
        elif self.has_been_visited:
            color = COLORS["passed"]
        else:
            color = COLORS[self.value]
        if self.frame is None:
            self.frame = tk.Frame(self.room, height=self.room.cell_height, width=self.room.cell_width, background=color)
        else:
            self.frame.configure(background=color)
        self.frame.grid(row=self.coordinates[0], column=self.coordinates[1])

    def __hash__(self):
        return hash(self.coordinates)


class RoomGui(tk.Tk):
    def __init__(self, aspirateur_class: Type[Aspirateur], room: List[str]):
        super().__init__()
        self.step_nbr = 0
        self.title("Laspirateur")
        self.active = True

        self.room = room
        self.cell_height = 20
        self.cell_width = 20

        self.cells = {}
        for i, row in enumerate(self.room):
            for j, cell in enumerate(row):
                self.cells[i, j] = Cell(self, cell, (i, j))
                self.cells[i, j].show()

        self.aspirateur: Aspirateur = aspirateur_class()

    def get_surroundings(self, cell: Cell) -> Dict[str, Cell]:
        surroundings = {}
        for name, direction in DIRECTIONS.items():
            surrounding: Cell = self.cells[(cell.coordinates[0] + direction[0], cell.coordinates[1] + direction[1])]
            if surrounding.value == " ":
                surroundings[name] = surrounding
        return surroundings

    def mainloop(self, n=0) -> None:
        aspirateur_cell: Cell = random.choice([cell for cell in self.cells.values() if cell.value == " "])
        aspirateur_cell.move_in(self.aspirateur)
        while self.active:
            self.step_nbr += 1
            self.update()
            aspirateur_cell.move_from(self.aspirateur)
            aspirateur_cell = self.aspirateur.choose_cell_to_move_in(self.get_surroundings(aspirateur_cell))
            aspirateur_cell.move_in(self.aspirateur)
            time.sleep(0.02)

    def destroy(self) -> None:
        print(f"Step number : {self.step_nbr}")
        visited_cells_nbr = sum(1 for cell in self.cells.values() if cell.has_been_visited)
        print(f"Score : {round((visited_cells_nbr ** 2 / (self.step_nbr * visited_cells_nbr)), 2)}")
        self.active = False


class Aspirateur:
    def choose_cell_to_move_in(self, surroundings: Dict[str, Cell]) -> Cell:
        raise NotImplementedError


class AspirateurRandom(Aspirateur):
    def __init__(self):
        self.last_cells = None, None

    def choose_cell_to_move_in(self, surroundings: Dict[str, Cell]) -> Cell:
        return random.choice(list(surroundings.values()))


class CleverAspirateur(Aspirateur):
    def __init__(self):
        self.coordinates = 0, 0
        self.passed = {self.coordinates: 0}

    def choose_cell_to_move_in(self, surroundings: Dict[str, Cell]) -> Cell:
        """
        surroundings : {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}
        surroundings contains only available directions
        """
        buffer = {}
        cp_surroundings = list(surroundings)
        random.shuffle(cp_surroundings)
        for next_direction in cp_surroundings:
            # compute relative coordinates of the direction
            coordinates = (
                self.coordinates[0] + DIRECTIONS[next_direction][0],
                self.coordinates[1] + DIRECTIONS[next_direction][1],
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


if __name__ == "__main__":
    from labygenerator import get_full_string_format_lab
    from rooms import *

    # app = RoomGui(CleverAspirateur, get_full_string_format_lab(random.randint(49, 50), random.randint(70, 71)))
    app = RoomGui(CleverAspirateur, room1)
    # app = RoomGui(CleverAspirateur, random.choice((room1, room2, room3, room4)))
    app.mainloop()
