DIRS = HAUT, BAS, GAUCHE, DROITE = (-1, 0), (1, 0), (0, -1), (0, 1)


class DansLeMurException(BaseException):
    pass


class Map:
    def __init__(self):
        self.map = (
            "MMMMMMMMMMMMMMMMMMMM",
            "MM    M         MM M",
            "M M      M  M      M",
            "M M M    M         M",
            "M M   M MMMM       M",
            "M   M M  M         M",
            "MMM M    M    MM   M",
            "M        M  M      M",
            "M M  M M M        MM",
            "M      M    M   M  M",
            "MMMMMMM        MM  M",
            "M  M       M       M",
            "M  M  MM      M    M",
            "M  M      MM       M",
            "MMMMMMMMMMMMMMMMMMMM",
        )
        self.agent_position = 3, 3
        self.passed = {self.agent_position: True}

    def get_voisins(self):
        for direction in DIRS:
            destination = (self.agent_position[0] + direction[0]), (self.agent_position[1] + direction[1])
            if (
                self.map[destination[0]][destination[1]] != "M"
                and self.map[destination[0]][destination[1]] not in self.passed
            ):
                self.passed[destination] = False
        voisins = {
            HAUT: self.map[self.agent_position[0] - 1][self.agent_position[1]],
            BAS: self.map[self.agent_position[0] + 1][self.agent_position[1]],
            GAUCHE: self.map[self.agent_position[0]][self.agent_position[1] - 1],
            DROITE: self.map[self.agent_position[0]][self.agent_position[1] + 1],
        }
        return voisins

    def move(self, direction):
        destination = (self.agent_position[0] + direction[0]), (self.agent_position[1] + direction[1])
        if self.map[destination[0]][destination[1]] == "M":
            raise DansLeMurException
        self.agent_position = destination
        self.passed[destination] = True


class Aspirateur:
    def __init__(self) -> None:
        self.piece = Map()

    def step(self):
        voisins = self.piece.get_voisins()
        self.piece.move(self.choice(voisins))

    def choice(self, voisins):
        pass
