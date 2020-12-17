from __future__ import annotations

import random
import time
import tkinter as tk
from collections import defaultdict
from typing import Dict, Type, List, Tuple

DIRECTIONS = {"UP": (-1, 0), "DOWN": (+1, 0), "LEFT": (0, -1), "RIGHT": (0, +1)}

PATH = " "
WALL = "M"

# COLORS = {"M": "#9c5959", " ": "#5ebeff", "aspirateur": "#768b99", "passed": "#306182"}
COLORS = {WALL: "#cc3300", PATH: "#99cc33", "aspirateur": "#ffcc00", "passed": "#339900", "invisible": "#000000"}


random.seed(0)


class Cell:
    def __init__(self, frame: tk.Frame, value: str, coordinates: Tuple[int, int]):
        self.value = value
        self.content = set()
        self.coordinates = coordinates
        self.has_been_visited = False
        self.frame = frame

    @property
    def is_passable(self):
        return self.value == PATH

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
        self.frame.configure(background=color)

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
            for j, cell_value in enumerate(row):
                cell = Cell(tk.Frame(self, height=self.cell_height, width=self.cell_width), cell_value, (i, j))
                cell.frame.grid(row=cell.coordinates[0], column=cell.coordinates[1])
                self.cells[i, j] = cell
                cell.show()

        self.aspirateur: Aspirateur = aspirateur_class()

    def get_nearby_path_cells(self, cell: Cell) -> Dict[str, Cell]:
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
            aspirateur_cell = self.aspirateur.choose_cell_to_move_in(self.get_nearby_path_cells(aspirateur_cell))
            aspirateur_cell.move_in(self.aspirateur)
            time.sleep(0.05)

    def destroy(self) -> None:
        print(f"Step number : {self.step_nbr}")
        visited_cells_nbr = sum(1 for cell in self.cells.values() if cell.has_been_visited)
        print(f"Score : {round((visited_cells_nbr ** 2 / (self.step_nbr * visited_cells_nbr)), 2)}")
        self.active = False


class Aspirateur:
    def choose_cell_to_move_in(self, surroundings: Dict[str, Cell]) -> Cell:
        raise NotImplementedError


class AspirateurRandom(Aspirateur):
    def choose_cell_to_move_in(self, surroundings: Dict[str, Cell]) -> Cell:
        return random.choice(list(surroundings.values()))


class CleverAspirateur(Aspirateur):
    def __init__(self):
        self.coordinates = 0, 0
        self.passed = defaultdict(int, {self.coordinates: 0})
        # todo : use cell as key

    def choose_cell_to_move_in(self, surroundings: Dict[str, Cell]) -> Cell:
        """
        surroundings : {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}
        surroundings contains only available directions
        """
        coordinates_of_surroundings = {}
        cp_surroundings = list(surroundings.keys())
        random.shuffle(cp_surroundings)
        for next_direction in cp_surroundings:
            # compute relative coordinates of the direction
            coordinates = (
                self.coordinates[0] + DIRECTIONS[next_direction][0],
                self.coordinates[1] + DIRECTIONS[next_direction][1],
            )
            coordinates_of_surroundings[next_direction] = coordinates
            if coordinates not in self.passed:
                # If we are never been in this cell, let's go into
                break
        else:
            # If break statement is not raised
            next_direction = min(surroundings, key=lambda x: self.passed[coordinates_of_surroundings[x]])
            coordinates = coordinates_of_surroundings[next_direction]
        self.coordinates = coordinates
        self.passed[self.coordinates] += 1
        # todo : do not assume we actually went into the selected cell
        return surroundings[next_direction]


if __name__ == "__main__":

    def main():
        from labygenerator import get_full_string_format_lab
        from rooms import room1

        # room = get_full_string_format_lab(30, 40)
        # room = get_full_string_format_lab(random.randint(49, 50), random.randint(70, 71))
        room = room1

        app = RoomGui(CleverAspirateur, room)
        # app = RoomGui(CleverAspirateur, random.choice((room1, room2, room3, room4)))
        app.mainloop()
        return locals()

    scope = main()
