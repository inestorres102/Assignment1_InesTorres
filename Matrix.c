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
    /* Standard triple-loop dense matrix multiplication O(n^3) */
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            C[i][j] = 0.0;
            for (int k = 0; k < n; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}



int check_correctness(int n) {
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

    for (int i = 0; i < n; i++) { free(A[i]); free(I[i]); free(C[i]); }
    free(A); free(I); free(C);
    return passed;
}



int main() {
    if (!check_correctness(10)) {
        fprintf(stderr, "Error: Validation failed in C.\n");
        return 1;
    }
    printf("Validation successful in C: A * I = A\n");

    int sizes[] = {50, 100, 200, 300, 400, 500, 600, 800, 1000};
    int num_sizes = sizeof(sizes) / sizeof(sizes[0]);
    int repetitions = 5;
    double timeout_seconds = 45.0;

    FILE *f_check = fopen("results.csv", "r");
    int write_header = (f_check == NULL);
    if (f_check) {
        fclose(f_check);
    }

    FILE *f = fopen("results.csv", "a");
    if (!f) {
        perror("Failed to open results.csv");
        return 1;
    }
    if (write_header) {
        fprintf(f, "language,n,repetition,time_seconds,memory_mb\n");
    }

    for (int s = 0; s < num_sizes; s++) {
        int n = sizes[s];
        printf("[C] Running n = %d...\n", n);

        // Dynamic heap allocation
        double **A = malloc(n * sizeof(double *));
        double **B = malloc(n * sizeof(double *));
        double **C = malloc(n * sizeof(double *));
        for (int i = 0; i < n; i++) {
            A[i] = malloc(n * sizeof(double));
            B[i] = malloc(n * sizeof(double));
            C[i] = malloc(n * sizeof(double));
        }

        // Discarded warm-up run
        generate_matrix(A, n, 1);
        generate_matrix(B, n, 2);
        multiply_matrices(A, B, C, n);

        int timed_out = 0;
        double mem_mb = (3.0 * n * n * sizeof(double)) / (1024.0 * 1024.0);

        for (int rep = 1; rep <= repetitions; rep++) {
            generate_matrix(A, n, 100 + rep);
            generate_matrix(B, n, 200 + rep);

            struct timespec start, end;
            clock_gettime(CLOCK_MONOTONIC, &start);

            multiply_matrices(A, B, C, n);

            clock_gettime(CLOCK_MONOTONIC, &end);
            double elapsed = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;

            fprintf(f, "C,%d,%d,%.6f,%.4f\n", n, rep, elapsed, mem_mb);
            fflush(f);

            if (elapsed > timeout_seconds) {
                printf("[C] n = %d exceeded timeout of %.1fs.\n", n, timeout_seconds);
                timed_out = 1;
                break;
            }
        }

        for (int i = 0; i < n; i++) {
            free(A[i]);
            free(B[i]);
            free(C[i]);
        }
        free(A);
        free(B);
        free(C);

        if (timed_out) {
            printf("[C] Stopping higher sizes due to execution time budget limit.\n");
            break;
        }
    }

    fclose(f);
    printf("[C] Benchmark completed successfully.\n");
    return 0;
}