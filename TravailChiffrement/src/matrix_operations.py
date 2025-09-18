# ==============================================
# matrix_operations.py
# ==============================================
# Projet : Opérations sur les matrices (Lester Hill Cipher)
# Objectif : Implémenter 3 fonctions :
#   1. Multiplication matrice × vecteur
#   2. Addition de matrices
#   3. Déterminant d’une matrice 2x2 et réversibilité modulo-n
#
# Chaque fonction est documentée et affiche les étapes du calcul.
# ==============================================

from math import gcd


# ------------------------------------------------
# 1. Multiplication d'une matrice par un vecteur
# ------------------------------------------------
def multiply_matrix_vector(matrix, vector):
    """
    Multiplie une matrice par un vecteur.
    
    Paramètres:
      matrix : liste de listes (matrice)
      vector : liste (vecteur)
      
    Retourne:
      result : liste (vecteur résultant)
    """
    if len(matrix[0]) != len(vector):
        raise ValueError("Nombre de colonnes de la matrice doit correspondre à la taille du vecteur")

    result = []
    for i, row in enumerate(matrix):
        total = 0
        print(f"--> Ligne {i+1}: {row}")
        for j in range(len(vector)):
            prod = row[j] * vector[j]
            print(f"    {row[j]} * {vector[j]} = {prod}")
            total += prod
        print(f"    Somme = {total}\n")
        result.append(total)
    return result


# ------------------------------------------------
# 2. Addition de deux matrices ou plus
# ------------------------------------------------
def add_matrices(*matrices):
    """
    Additionne plusieurs matrices de même dimension.
    
    Paramètres:
      matrices : une ou plusieurs matrices (listes de listes)
      
    Retourne:
      result : matrice somme
    """
    rows = len(matrices[0])
    cols = len(matrices[0][0])
    result = [[0 for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            elems = [m[i][j] for m in matrices]
            element_sum = sum(elems)
            print(f"--> Somme des éléments à la position ({i+1},{j+1}) {elems} = {element_sum}")
            result[i][j] = element_sum
    print()
    return result


# ------------------------------------------------
# 3. Déterminant d’une matrice 2x2 et réversibilité
# ------------------------------------------------
def determinant_2x2(matrix, modulo=None):
    """
    Calcule le déterminant d'une matrice 2x2 et teste sa réversibilité mod-n.
    
    Paramètres:
      matrix : liste de listes (matrice 2x2)
      modulo : entier (optionnel, valeur du modulo)
      
    Retourne:
      (det, reversible) : tuple avec le déterminant et un booléen (ou None si pas de modulo)
    """
    if len(matrix) != 2 or len(matrix[0]) != 2:
        raise ValueError("La matrice doit être 2x2")

    a, b = matrix[0]
    c, d = matrix[1]
    det = a*d - b*c
    print(f"--> Calcul du déterminant : {a}*{d} - {b}*{c} = {det}")

    reversible = None
    if modulo:
        reversible = gcd(det, modulo) == 1
        print(f"    Réversibilité modulo {modulo} : {reversible}")

    return det, reversible


# ------------------------------------------------
# Bloc de test (exécuté seulement si on lance ce fichier directement)
# ------------------------------------------------
if __name__ == "__main__":
    m1 = [[1, 2], [3, 4]]
    m2 = [[5, 6], [7, 8]]
    v = [5, 6]

    print("\n=== Multiplication matrice x vecteur ===")
    print("Résultat :", multiply_matrix_vector(m1, v))

    print("\n=== Addition de matrices ===")
    print("Résultat :", add_matrices(m1, m2))

    print("\n=== Déterminant et réversibilité ===")
    print("Résultat :", determinant_2x2(m1, modulo=26))
