import random

from agents import CleverAgent, RandomAgent
from engine import RoomGui
from labygenerator import get_full_string_format_lab
from rooms import *


def main():
    random.seed(0)

    # room = get_full_string_format_lab(5, 5)
    # room = get_full_string_format_lab(random.randint(49, 50), random.randint(70, 71))
    room = get_full_string_format_lab(30, 30)
    # room = room2
    # room = random.choice((room1, room2, room3, room4))

    agent = CleverAgent
    # agent = RandomAgent

    app = RoomGui(agent, room, 0.01, False)
    app.mainloop()
    return locals()


scope = main()
