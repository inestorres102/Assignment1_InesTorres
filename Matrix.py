import time
import random

def generate_matrix(n, seed):
    """Genera una matriz n x n con valores aleatorios."""
    random.seed(seed)
    return [[random.random() for _ in range(n)] for _ in range(n)]

def multiply_matrices(A, B, n):
    """Triple bucle clásico O(n^3) para multiplicar matrices."""
    # Inicializar matriz C con ceros
    C = [[0.0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

if __name__ == "__main__":
    n = 100  # Tamaño inicial de prueba
    A = generate_matrix(n, 42)
    B = generate_matrix(n, 43)

    # Medición básica del kernel
    start_time = time.time()
    C = multiply_matrices(A, B, n)
    end_time = time.time()

    print(f"Python: Matriz {n}x{n} calculada en {end_time - start_time:.5f} segundos")