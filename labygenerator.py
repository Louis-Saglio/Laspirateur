from random import seed, randint
from typing import List


seed(1)

WALL = "M"
BORDER = "B"
PLAYER = "X"
EXIT = "A"
PATH = " "


def random_generator(start, stop, size):
    buffer = [randint(start, stop) for _ in range(size)]
    while True:
        for i in buffer[randint(0, len(buffer) - 1) :]:
            yield i


RANDOM_GENERATOR = random_generator(0, 2, 2000)


def get_nearby_cells(maze, h, w):
    return [maze[h - 1][w], maze[h + 1][w], maze[h][w - 1], maze[h][w + 1]]


def create_maze(height: int, width: int, wall: str = WALL, path: str = PATH, border: str = BORDER):
    step_nbr = round(height * width * 0.15)
    path_is_complete = False
    height_minus_one, width_minus_one = height - 1, width - 1
    while not path_is_complete:
        maze = [[wall for __ in range(width)] for _ in range(height)]
        for h in range(height_minus_one):
            maze[h][0] = border
            maze[h][width_minus_one] = border
        for w in range(width_minus_one):
            maze[0][w] = border
            maze[height_minus_one][w] = border
        maze[1][1] = "X"
        for i in range(step_nbr):
            for h in range(height_minus_one):
                for w in range(width_minus_one):
                    if (maze[h][w] != border) and (next(RANDOM_GENERATOR) == 0):
                        nearby_cells = get_nearby_cells(maze, h, w)
                        if nearby_cells.count(wall) + nearby_cells.count(border) == 3:
                            maze[h][w] = path
        maze[1][1] = PLAYER
        maze[len(maze) - 2][len(maze[0]) - 2] = EXIT
        if get_nearby_cells(maze, height - 2, width-2).count(path):
            path_is_complete = True
    # noinspection PyUnboundLocalVariable
    return maze


def get_full_string_format_lab(height, width) -> List[str]:
    return ["".join(row).replace("B", "M").replace("A", " ").replace("X", " ") for row in create_maze(height, width)]


if __name__ == "__main__":
    from time import time

    start = time()
    for _ in range(1000):
        create_maze(20, 20)
    print(round(time() - start, 3))
