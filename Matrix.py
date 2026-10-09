import time
import random
import csv
import os
import random
import tracemalloc

def generate_matrix(n, seed):
    """n x n matrix -> random values"""
    random.seed(seed)
    return [[random.random() for _ in range(n)] for _ in range(n)]

def multiply_matrices(A, B, n):
    """standard triple-loop dense matrix multiplication O(n^3)"""
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
                print("Validation error in Python")
                return False
    print("Successful validation in Python: A * I = A")
    return True


def run_benchmark():
    if not check_correctness(10):
        print("Error: Validation failed in Python.")
        return

    print("Validation successful in Python: A * I = A")

    sizes = [50, 100, 200, 300, 400, 500]
    repetitions = 5
    timeout_seconds = 45.0
    csv_file = "results.csv"

    write_header = not os.path.exists(csv_file)
    with open(csv_file, mode="a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["language", "n", "repetition", "time_seconds", "memory_mb"])

        for n in sizes:
            print(f"[Python] Running n = {n}...")
            # Discarded warm-up run
            A_warm = generate_matrix(n, 1)
            B_warm = generate_matrix(n, 2)
            multiply_matrices(A_warm, B_warm, n)

            timed_out = False
            for rep in range(1, repetitions + 1):
                A = generate_matrix(n, 100 + rep)
                B = generate_matrix(n, 200 + rep)

                tracemalloc.start()
                start = time.perf_counter()
                C = multiply_matrices(A, B, n)
                elapsed = time.perf_counter() - start
                _, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                mem_mb = peak / (1024 * 1024)
                writer.writerow(["Python", n, rep, f"{elapsed:.6f}", f"{mem_mb:.4f}"])
                f.flush()

                if elapsed > timeout_seconds:
                    print(f"[Python] n = {n} exceeded timeout of {timeout_seconds}s.")
                    timed_out = True
                    break

            if timed_out:
                print("[Python] Stopping higher sizes due to execution time budget limit.")
                break

    print("[Python] Benchmark completed successfully.")

if __name__ == "__main__":
    run_benchmark()