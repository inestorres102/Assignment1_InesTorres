# Assignment 1: Basic Matrix Multiplication in Python, Java, and C

Empirical benchmark comparing naive dense matrix multiplication algorithms across Python, Java, and C under controlled experimental conditions.

## 1. System and Hardware Environment
- **CPU:** 12th Gen Intel(R) Core(TM) i7 - 12650H
- **RAM:** 16.0 GB DDR4
- **Operating System:** Windows 11
- **Compilers and Runtime Versions:**
  - Python: 3.14.0
  - Java: OpenJDK
  - C: GCC (MinGW)

## 2. Experimental Protocol
- **Algorithm:** Naive dense matrix multiplication with $O(n^3)$ arithmetic operations.
- **Matrix Dimensions ($n$):** Increasing sequence from $n = 50$ up to $n = 1000$.
- **Repetitions:** 1 warm-up run (excluded) followed by 5 recorded iterations per configuration.
- **Budget Limits:** 45.0 seconds execution timeout per multiplication kernel.
- **Correctness:** Verified against identity matrices ($A \times I = A$) with a numerical tolerance of $\varepsilon = 10^{-9}$.

## 3. Build and Execution Instructions

### Python
Ensure Python 3 is installed:
```bash
python Matrix.py
```

### Java
Ensure JDK 17 or higher is installed and configured in your PATH:

1. Compilation to bytecode:
```bash
javac Matrix.java
```

2. Execution on the HotSpot JVM:
```bash
java Matrix
```

### C
Ensure GCC is installed via MinGW, MSYS2, or WSL/Linux:

1. Compilation without optimization (baseline -O0):
```bash
gcc Matrix.c -o Matrix -lm
```

2. Compilation with optimization (-O3):
```bash
gcc -O3 Matrix.c -o Matrix -lm
```
*(Note: The `-lm` flag is required to link the C standard math library for `fabs` validation)*

3. Execution:
- Windows PowerShell:
```powershell
.\Matrix.exe
```
- Windows Command Prompt (CMD):
```cmd
Matrix.exe
```
- Linux / WSL / Git Bash:
```bash
./Matrix
```

## 4. Output Format and Raw Data (`results.csv`)
Benchmark executions automatically append observations to `results.csv` using the following schema:
- `language`: Target runtime environment (`Python`, `Java`, `C`).
- `n`: Side length of the square matrix ($n \times n$).
- `repetition`: Measured iteration index (1 to 5).
- `time_seconds`: Monotonic kernel elapsed execution time in seconds.
- `memory_mb`: Language-specific memory metric reported in megabytes (MB).

### Memory Metrics Description
- **Python:** Peak resident memory allocated during the multiplication kernel, tracked via `tracemalloc`.
- **Java:** Net heap memory differential sampled before and after execution via `Runtime.getRuntime()`.
- **C:** Theoretical dense array storage footprint ($3 \times n^2 \times 8$ bytes) required for input and result matrices.

## 5. Repository File Structure
```text
Assignment1/
├── .gitignore          # Excludes compiled binaries (.class, .exe), objects, and environments
├── README.md           # Reproduction instructions and experimental setup
├── Matrix.py           # Python naive implementation and benchmark harness
├── Matrix.java         # Java naive implementation and benchmark harness
├── Matrix.c            # C naive implementation and benchmark harness
└── results.csv         # Raw experimental measurements across all languages
```

