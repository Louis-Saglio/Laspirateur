from random import seed, randint
from typing import List


seed(1)

WALL = "M"
BORDER = "B"
START = "X"
FINNISH = "A"


def random_generator(start, stop, size):
    buffer = [randint(start, stop) for _ in range(size)]
    while True:
        for i in buffer[randint(0, len(buffer) - 1):]:
            yield i


RANDOM_GENERATOR = random_generator(0, 2, 500)


def dessiner_bordure(matrice, bordure="B"):
    hauteur = len(matrice)
    largeur = len(matrice[0])
    for h in range(hauteur):
        matrice[h][0] = bordure
        matrice[h][largeur - 1] = bordure
    for l in range(largeur):
        matrice[0][l] = bordure
        matrice[hauteur - 1][l] = bordure
    return matrice


def placer_depart_arrivee(matrice):
    matrice[1][1] = "X"
    matrice[len(matrice) - 2][len(matrice[0]) - 2] = "A"
    return matrice


def get_nbr_of_neighbours_of_type(matrix, h, l, case_type):
    return [
        matrix[h - 1][l],  # en-haut
        matrix[h + 1][l],  # en-bas
        matrix[h][l - 1],  # à gauche
        matrix[h][l + 1],  # à droite
    ].count(case_type)


def determiner_si_devenir_chemin(matrice, h, l, mur, bordure):
    do = True
    if matrice[h][l] == bordure:
        do = False
    elif next(RANDOM_GENERATOR) != 0:
        do = False
    elif get_nbr_of_neighbours_of_type(matrice, h, l, mur) + get_nbr_of_neighbours_of_type(matrice, h, l, bordure) != 3:
        do = False
    return do


def creer_chemin(matrice, mur, chemin, bordure):
    hauteur = len(matrice)
    largeur = len(matrice[0])
    for h in range(hauteur - 1):
        for l in range(largeur - 1):
            if determiner_si_devenir_chemin(matrice, h, l, mur, bordure) is True:
                matrice[h][l] = chemin
    return matrice


def creer_laby(hauteur=15, largeur=15, wall="M"):
    nbr_tours = round(((hauteur * largeur) / 10) * 1.5)
    chemin_fini = False
    while chemin_fini is False:
        mat = [[wall for __ in range(largeur)] for _ in range(hauteur)]
        mat = dessiner_bordure(mat)
        mat[1][1] = 0
        for i in range(nbr_tours):
            mat = creer_chemin(mat, "M", " ", "B")
        mat = placer_depart_arrivee(mat)
        if get_nbr_of_neighbours_of_type(mat, len(mat) - 2, len(mat[0]) - 2, " ") > 0:
            chemin_fini = True
        else:
            nbr_tours += 20
    return mat


def get_full_string_format_lab(height, width) -> List[str]:
    return ["".join(row).replace("B", "M").replace("A", " ").replace("X", " ") for row in creer_laby(height, width)]


if __name__ == "__main__":
    from time import time

    start = time()
    for _ in range(1):
        creer_laby(100, 100)
    print(round(time() - start, 3))
