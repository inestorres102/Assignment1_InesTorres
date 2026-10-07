#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

void generate_matrix(double **matrix, int n, int seed) {
    srand(seed);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            matrix[i][j] = (double)rand() / RAND_MAX;
        }
    }
}

void multiply_matrices(double **A, double **B, double **C, int n) {
    /* Triple bucle clásico O(n^3) */
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            C[i][j] = 0.0;
            for (int k = 0; k < n; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}



// Validación previa
void check_correctness(int n) {
    double **A = malloc(n * sizeof(double *));
    double **I = malloc(n * sizeof(double *));
    double **C = malloc(n * sizeof(double *));
    for (int i = 0; i < n; i++) {
        A[i] = malloc(n * sizeof(double));
        I[i] = malloc(n * sizeof(double));
        C[i] = malloc(n * sizeof(double));
        for (int j = 0; j < n; j++) {
            I[i][j] = (i == j) ? 1.0 : 0.0;
        }
    }
    
    generate_matrix(A, n, 42);
    multiply_matrices(A, I, C, n);
    
    double epsilon = 1e-9;
    int passed = 1;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (fabs(C[i][j] - A[i][j]) > epsilon) passed = 0;
        }
    }
    
    if (passed) printf("Validación exitosa en C: A * I = A\n");
    else printf("Error de validación en C.\n");
    
    for (int i = 0; i < n; i++) { free(A[i]); free(I[i]); free(C[i]); }
    free(A); free(I); free(C);
}




int main() {
    int n = 100; // Tamaño inicial de prueba

    // Asignación de memoria en el Heap
    double **A = malloc(n * sizeof(double *));
    double **B = malloc(n * sizeof(double *));
    double **C = malloc(n * sizeof(double *));
    for (int i = 0; i < n; i++) {
        A[i] = malloc(n * sizeof(double));
        B[i] = malloc(n * sizeof(double));
        C[i] = malloc(n * sizeof(double));
    }

    // Generar datos fuera de la región cronometrada
    generate_matrix(A, n, 42);
    generate_matrix(B, n, 43);

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    // Ejecución del kernel
    multiply_matrices(A, B, C, n);

    clock_gettime(CLOCK_MONOTONIC, &end);
    double time_taken = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;

    printf("C: Matriz %dx%d calculada en %.5f segundos\n", n, n, time_taken);

    // Liberar memoria
    for (int i = 0; i < n; i++) {
        free(A[i]); free(B[i]); free(C[i]);
    }
    free(A); free(B); free(C);

    return 0;
}