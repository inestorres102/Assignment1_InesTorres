import java.util.Random;

public class Matrix {

    public static double[][] generateMatrix(int n, long seed) {
        Random rand = new Random(seed);
        double[][] matrix = new double[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                matrix[i][j] = rand.nextDouble();
            }
        }
        return matrix;
    }

    public static double[][] multiplyMatrices(double[][] A, double[][] B, int n) {
        /* Triple bucle clásico O(n^3) */
        double[][] C = new double[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                for (int k = 0; k < n; k++) {
                    C[i][j] += A[i][k] * B[k][j];
                }
            }
        }
        return C;
    }

    public static void main(String[] args) {
        int n = 100; // Tamaño inicial de prueba
        
        // Generar datos fuera de la región cronometrada
        double[][] A = generateMatrix(n, 42L);
        double[][] B = generateMatrix(n, 43L);

        long startTime = System.nanoTime();
        
        // Ejecución del kernel
        double[][] C = multiplyMatrices(A, B, n);
        
        long endTime = System.nanoTime();

        double timeTaken = (endTime - startTime) / 1e9;
        System.out.printf("Java: Matriz %dx%d calculada en %.5f segundos\n", n, n, timeTaken);
    }
}