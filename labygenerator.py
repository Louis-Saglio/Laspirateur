def creer_matrice(hauteur=15, largeur=25, remplissage='M'):
    matrice = []
    for i in range(hauteur):
        matrice.append([])
        for c in range(largeur):
            matrice[i].append(remplissage)
    return matrice


def dessiner_bordure(matrice, bordure='B'):
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
    matrice[1][1] = 'X'
    matrice[len(matrice) - 2][len(matrice[0]) - 2] = 'A'
    return matrice


def renvoyer_cases_contact(matrice, h, l, case):
    contacts = [
        matrice[h - 1][l],  # en-haut
        matrice[h + 1][l],  # en-bas
        matrice[h][l - 1],  # à gauche
        matrice[h][l + 1]  # à droite
    ]
    return contacts.count(case)


def determiner_si_devenir_chemin(matrice, h, l, mur, chemin, bordure):
    from random import randint
    rand, contact, bord = False, False, False
    if randint(0, 2) == 0:
        rand = True
    if renvoyer_cases_contact(matrice, h, l, mur) + renvoyer_cases_contact(matrice, h, l, bordure) == 3:
        contact = True
    if matrice[h][l] != bordure:
        bord = True
    return rand and contact and bord


def creer_chemin(matrice, mur, chemin, bordure):
    hauteur = len(matrice)
    largeur = len(matrice[0])
    for h in range(hauteur - 1):
        for l in range(largeur - 1):
            if determiner_si_devenir_chemin(matrice, h, l, mur, chemin, bordure) is True:
                matrice[h][l] = chemin
    return matrice


def creer_laby(hauteur=15, largeur=15):
    nbrTours = round(((hauteur * largeur) / 10) * 1.5)
    chemin_fini = False
    while chemin_fini is False:
        mat = creer_matrice(hauteur, largeur)
        mat = dessiner_bordure(mat)
        mat[1][1] = 0
        for i in range(nbrTours):
            mat = creer_chemin(mat, 'M', ' ', 'B')
        mat = placer_depart_arrivee(mat)
        if renvoyer_cases_contact(mat, len(mat) - 2, len(mat[0]) - 2, ' ') > 0:
            chemin_fini = True
        else:
            nbrTours += 20
    return mat


def get_full_string_format_lab(height, width):
    return [''.join(row).replace('B', 'M').replace('A', ' ').replace('X', ' ') for row in creer_laby(height, width)]
