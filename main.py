from agent import CleverAgent, RandomAgent
from engine import RoomGui


def main():
    from rooms import room1

    # room = get_full_string_format_lab(30, 40)
    # room = get_full_string_format_lab(random.randint(49, 50), random.randint(70, 71))
    room = room1
    # room = random.choice((room1, room2, room3, room4))

    agent = CleverAgent
    # agent = RandomAgent

    app = RoomGui(agent, room, 0.05)
    app.mainloop()
    return locals()


scope = main()
