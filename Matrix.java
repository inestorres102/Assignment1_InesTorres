import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.Locale;
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
        /* Standard triple-loop dense matrix multiplication O(n^3) */
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



    public static boolean checkCorrectness(int n) {
        /* Validates the multiplication against an identity matrix (A * I = A) */
        double[][] A = generateMatrix(n, 42L);
        double[][] I = new double[n][n];
        for (int i = 0; i < n; i++) {
            I[i][i] = 1.0;
        }
        double[][] C = multiplyMatrices(A, I, n);
        double epsilon = 1e-9;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (Math.abs(C[i][j] - A[i][j]) > epsilon) {
                    return false;
                }
            }
        }
        return true;
    }

    public static void main(String[] args) {
        if (!checkCorrectness(10)) {
            System.err.println("Error: Validation failed in Java.");
            return;
        }
        System.out.println("Validation successful in Java: A * I = A");

        int[] sizes = {50, 100, 200, 300, 400, 500, 600, 800, 1000};
        int repetitions = 5;
        double timeoutSeconds = 45.0;
        String csvFile = "results.csv";

        try {
            boolean writeHeader = !(new File(csvFile).exists());
            PrintWriter writer = new PrintWriter(new FileWriter(csvFile, true));
            if (writeHeader) {
                writer.println("language,n,repetition,time_seconds,memory_mb");
            }

            Runtime runtime = Runtime.getRuntime();

            for (int n : sizes) {
                System.out.printf("[Java] Running n = %d...\n", n);

                // Discarded warm-up run
                double[][] Aw = generateMatrix(n, 1L);
                double[][] Bw = generateMatrix(n, 2L);
                multiplyMatrices(Aw, Bw, n);

                boolean timedOut = false;
                for (int rep = 1; rep <= repetitions; rep++) {
                    double[][] A = generateMatrix(n, 100L + rep);
                    double[][] B = generateMatrix(n, 200L + rep);

                    System.gc();
                    long memBefore = runtime.totalMemory() - runtime.freeMemory();

                    long start = System.nanoTime();
                    double[][] C = multiplyMatrices(A, B, n);
                    long duration = System.nanoTime() - start;

                    long memAfter = runtime.totalMemory() - runtime.freeMemory();
                    double memMb = Math.max(0, memAfter - memBefore) / (1024.0 * 1024.0);
                    if (memMb <= 0.01) {
                        memMb = (double) (n * n * 8L) / (1024.0 * 1024.0);
                    }

                    double elapsedSec = duration / 1.0e9;
                    writer.printf(Locale.US, "Java,%d,%d,%.6f,%.4f\n", n, rep, elapsedSec, memMb);
                    writer.flush();

                    if (elapsedSec > timeoutSeconds) {
                        System.out.printf("[Java] n = %d exceeded timeout of %.1fs.\n", n, timeoutSeconds);
                        timedOut = true;
                        break;
                    }
                }

                if (timedOut) {
                    System.out.println("[Java] Stopping higher sizes due to execution time budget limit.");
                    break;
                }
            }
            writer.close();
            System.out.println("[Java] Benchmark completed successfully.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}