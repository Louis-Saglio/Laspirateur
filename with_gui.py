from __future__ import annotations

import random
import time
import tkinter as tk
from typing import Literal, Type, Union

from agent_interface import Agent

DIRECTIONS = {"UP": (-1, 0), "DOWN": (+1, 0), "LEFT": (0, -1), "RIGHT": (0, +1)}

# COLORS = {"M": "#9c5959", " ": "#5ebeff", "agent": "#768b99", "passed": "#306182"}
COLORS = {"M": "#cc3300", " ": "#99cc33", "agent": "#ffcc00", "passed": "#339900", "invisible": "#000000"}


random.seed(1)


class Cell:
    def __init__(self, frame: tk.Frame, value: Literal["M", " "], coordinates: tuple[int, int], is_being_seen=False):
        self.value = value
        self.content = set()
        self.coordinates = coordinates
        self.has_been_visited = False
        self._is_being_seen = is_being_seen
        self.frame = frame

    @property
    def is_being_seen(self):
        return self._is_being_seen

    @is_being_seen.setter
    def is_being_seen(self, value):
        self._is_being_seen = value
        self.show()

    def move_in(self, pawn: object) -> None:
        self.content.add(pawn)
        self.has_been_visited = True
        self.show()

    def move_from(self, pawn: object) -> None:
        self.content.remove(pawn)
        self.show()

    def contains_agent(self) -> bool:
        for item in self.content:
            if isinstance(item, Agent):
                return True
        return False

    def show(self) -> None:
        if self.contains_agent():
            color = COLORS["agent"]
        elif not self.is_being_seen:
            color = COLORS["invisible"]
        elif self.has_been_visited:
            color = COLORS["passed"]
        else:
            color = COLORS[self.value]
        self.frame.configure(background=color)

    def __hash__(self):
        return hash(self.coordinates)


class RoomGui(tk.Tk):
    def __init__(
        self,
        agent_class: Type[Agent],
        room: list[Literal[" ", "M"]],
        delay: Union[int, float],
        hide_invisible_cells=False,
    ):
        super().__init__()
        self.step_nbr = 0
        self.title("agent")
        self.active = True

        self.room = room
        self.cell_height = 20
        self.cell_width = 20

        self.delay = delay
        self.hide_invisible_cells = hide_invisible_cells

        self.cells = {}
        for i, row in enumerate(self.room):
            for j, cell_value in enumerate(row):
                cell = Cell(
                    tk.Frame(self, height=self.cell_height, width=self.cell_width),
                    cell_value,
                    (i, j),
                    is_being_seen=not hide_invisible_cells,
                )
                cell.frame.grid(row=cell.coordinates[0], column=cell.coordinates[1])
                self.cells[i, j] = cell
                cell.show()

        self.agent: Agent = agent_class()

    def mainloop(self, n=0) -> None:
        agent_cell: Cell = random.choice([cell for cell in self.cells.values() if cell.value == " "])
        agent_cell.move_in(self.agent)
        while self.active:
            self.step_nbr += 1
            nearby_path_cells = {}
            nearby_cells = []
            for name, direction in DIRECTIONS.items():
                cell: Cell = self.cells[
                    (agent_cell.coordinates[0] + direction[0], agent_cell.coordinates[1] + direction[1])
                ]
                if self.hide_invisible_cells:
                    nearby_cells.append(cell)
                    cell.is_being_seen = True
                if cell.value == " ":
                    nearby_path_cells[name] = cell
            self.update()
            time.sleep(self.delay)
            agent_cell.move_from(self.agent)
            agent_cell = self.agent.choose_cell_to_move_in(nearby_path_cells)
            agent_cell.move_in(self.agent)
            self.update()
            if self.hide_invisible_cells:
                for cell in nearby_cells:
                    cell.is_being_seen = False

    def destroy(self) -> None:
        print(f"Step number : {self.step_nbr}")
        visited_cells_nbr = sum(1 for cell in self.cells.values() if cell.has_been_visited)
        print(f"Score : {round((visited_cells_nbr ** 2 / (self.step_nbr * visited_cells_nbr)), 2)}")
        self.active = False
