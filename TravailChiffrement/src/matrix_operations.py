# ==============================================
# matrix_operations.py
# ==============================================
# Projet : Opérations sur les matrices (Lester Hill Cipher)
# Objectif : Implémenter 3 fonctions :
#   1. Multiplication matrice × vecteur
#   2. Addition de matrices
#   3. Déterminant d’une matrice 2x2 et réversibilité modulo-n
#
# Ajout : Un menu interactif + gestion des erreurs
# ==============================================

from math import gcd


# ------------------------------------------------
# 1. Multiplication d'une matrice par un vecteur
# ------------------------------------------------
def multiply_matrix_vector(matrix, vector):
    if len(matrix[0]) != len(vector):
        raise ValueError("❌ Nombre de colonnes de la matrice doit correspondre à la taille du vecteur")

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
    if len(matrix) != 2 or len(matrix[0]) != 2:
        raise ValueError("❌ La matrice doit être 2x2")

    a, b = matrix[0]
    c, d = matrix[1]
    det = a * d - b * c
    print(f"--> Calcul du déterminant : {a}*{d} - {b}*{c} = {det}")

    reversible = None
    if modulo:
        reversible = gcd(det, modulo) == 1
        print(f"    Réversibilité modulo {modulo} : {reversible}")

    return det, reversible


# ------------------------------------------------
# Menu interactif avec gestion des erreurs
# ------------------------------------------------
def menu():
    while True:
        print("\n=== MENU ===")
        print("1. Multiplication matrice × vecteur")
        print("2. Addition de matrices")
        print("3. Déterminant 2x2 et réversibilité mod-n")
        print("4. Quitter")

        choice = input("Choisis une option (1-4): ")

        try:
            if choice == "1":
                rows = int(input("Nombre de lignes de la matrice: "))
                cols = int(input("Nombre de colonnes de la matrice: "))
                matrix = []
                for i in range(rows):
                    row = list(map(int, input(f"Ligne {i+1} (séparer les nombres par espace): ").split()))
                    if len(row) != cols:
                        raise ValueError("❌ Nombre de colonnes incorrect")
                    matrix.append(row)
                vector = list(map(int, input(f"Vecteur de taille {cols} (séparer par espace): ").split()))
                if len(vector) != cols:
                    raise ValueError("❌ Taille du vecteur incorrecte")
                print("✅ Résultat :", multiply_matrix_vector(matrix, vector))

            elif choice == "2":
                nb_matrices = int(input("Combien de matrices veux-tu additionner? "))
                matrices = []
                for k in range(nb_matrices):
                    print(f"--- Matrice {k+1} ---")
                    rows = int(input("Nombre de lignes: "))
                    cols = int(input("Nombre de colonnes: "))
                    matrix = []
                    for i in range(rows):
                        row = list(map(int, input(f"Ligne {i+1}: ").split()))
                        if len(row) != cols:
                            raise ValueError("❌ Nombre de colonnes incorrect")
                        matrix.append(row)
                    matrices.append(matrix)
                print("✅ Résultat :", add_matrices(*matrices))

            elif choice == "3":
                print("--- Matrice 2x2 ---")
                row1 = list(map(int, input("Première ligne (2 nombres): ").split()))
                row2 = list(map(int, input("Deuxième ligne (2 nombres): ").split()))
                if len(row1) != 2 or len(row2) != 2:
                    raise ValueError("❌ Chaque ligne doit contenir exactement 2 nombres")
                matrix = [row1, row2]
                modulo = int(input("Modulo (ou 0 si pas de modulo): "))
                modulo = modulo if modulo != 0 else None
                print("✅ Résultat :", determinant_2x2(matrix, modulo))

            elif choice == "4":
                print("👋 Au revoir")
                break

            else:
                print("⚠️ Choix invalide, réessaye.")

        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"⚠️ Erreur inattendue : {e}")


# ------------------------------------------------
# Lancement du programme
# ------------------------------------------------
if __name__ == "__main__":
    menu()
