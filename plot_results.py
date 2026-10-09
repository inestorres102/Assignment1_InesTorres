import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

csv_file = "results.csv"
if not os.path.exists(csv_file):
    print(f"Error: No se encuentra '{csv_file}' en el directorio actual.")
    exit(1)

# 1. Cargar mediciones
df = pd.read_csv(csv_file)

# 2. Resumen estadístico: Mediana y Rango Intercuartílico (IQR)
summary = df.groupby(["language", "n"])["time_seconds"].agg(
    median="median",
    q25=lambda x: np.percentile(x, 25),
    q75=lambda x: np.percentile(x, 75)
).reset_index()

summary["iqr"] = summary["q75"] - summary["q25"]

print("\n=== TABLA DE RESUMEN ESTADÍSTICO (TIEMPO EN SEGUNDOS) ===")
print(summary[["language", "n", "median", "iqr"]].to_string(index=False))

summary.to_csv("summary_statistics.csv", index=False)

# 3. Gráfica 1: Escalabilidad temporal (Log-Log)
plt.figure(figsize=(8, 5))
for lang in summary["language"].unique():
    data = summary[summary["language"] == lang]
    plt.errorbar(
        data["n"],
        data["median"],
        yerr=data["iqr"],
        label=lang,
        marker="o",
        capsize=4
    )

plt.xscale("log")
plt.yscale("log")
plt.xlabel("Matrix Dimension ($n$)", fontsize=11)
plt.ylabel("Execution Time (seconds, log scale)", fontsize=11)
plt.title("Matrix Multiplication Kernel Runtime vs. Dimension $n$", fontsize=12)
plt.grid(True, which="both", linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("time_comparison_loglog.png", dpi=300)
plt.show()

# 4. Gráfica 2: Huella de memoria
mem_summary = df.groupby(["language", "n"])["memory_mb"].median().reset_index()

plt.figure(figsize=(8, 5))
for lang in mem_summary["language"].unique():
    data = mem_summary[mem_summary["language"] == lang]
    plt.plot(data["n"], data["memory_mb"], label=f"{lang} Memory", marker="s")

plt.xlabel("Matrix Dimension ($n$)", fontsize=11)
plt.ylabel("Reported Memory (MB)", fontsize=11)
plt.title("Memory Footprint vs. Matrix Dimension $n$", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("memory_comparison.png", dpi=300)
plt.show()

print("\nArchivos guardados en el directorio:")
print("- 'time_comparison_loglog.png'")
print("- 'memory_comparison.png'")
print("- 'summary_statistics.csv'")