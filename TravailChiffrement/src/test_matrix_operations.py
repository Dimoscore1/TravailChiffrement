from matrix_operations import multiply_matrix_vector, add_matrices, determinant_2x2

def test_multiply():
    A = [[1, 2], [3, 4]]
    v = [5, 6]
    result = multiply_matrix_vector(A, v)
    print("Multiplication:", result)

def test_add():
    A = [[1, 2], [3, 4]]
    B = [[2, 1], [0, 3]]
    result = add_matrices(A, B)
    print("Addition:", result)

def test_determinant():
    A = [[1, 2], [3, 4]]
    result = determinant_2x2(A)
    print("Déterminant:", result)

# Lancer tous les tests
if __name__ == "__main__":
    test_multiply()
    test_add()
    test_determinant()
