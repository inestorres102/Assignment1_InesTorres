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


# Validación previa
def check_correctness(n):
    # Crear matriz identidad
    I = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    # Matriz aleatoria A
    A = generate_matrix(n, 42)
    
    # Multiplicar A * I
    C = multiply_matrices(A, I, n)
    
    # Validar con tolerancia (1e-9)
    epsilon = 1e-9
    for i in range(n):
        for j in range(n):
            if abs(C[i][j] - A[i][j]) > epsilon:
                print("Error de validación en Python.")
                return False
    print("Validación exitosa en Python: A * I = A")
    return True

# Ejecución de validación, previa a la ejecución ppal
if __name__ == "__main__":
    check_correctness(10) # Prueba de correctness obligatoria


if __name__ == "__main__":
    n = 100  # Tamaño inicial de prueba
    A = generate_matrix(n, 42)
    B = generate_matrix(n, 43)

    # Medición básica del kernel
    start_time = time.time()
    C = multiply_matrices(A, B, n)
    end_time = time.time()

    print(f"Python: Matriz {n}x{n} calculada en {end_time - start_time:.5f} segundos")