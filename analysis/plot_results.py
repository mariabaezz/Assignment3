import csv
from collections import defaultdict
from pathlib import Path
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "results" / "summary_results.csv"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

rows = []
with SUMMARY.open() as f:
    for r in csv.DictReader(f):
        r["n"] = int(r["n"])
        r["threads"] = int(r["threads"])
        r["median_time_s"] = float(r["median_time_s"])
        r["speedup"] = float(r["speedup"])
        r["efficiency"] = float(r["efficiency"])
        rows.append(r)

# Runtime vs thread count for each n
for n in sorted({r["n"] for r in rows}):
    omp = sorted(
        [r for r in rows if r["n"] == n and r["method"] == "omp"],
        key=lambda r: r["threads"]
    )
    plt.figure()
    plt.plot([r["threads"] for r in omp], [r["median_time_s"] for r in omp], marker="o")
    plt.xlabel("Threads")
    plt.ylabel("Median runtime (s)")
    plt.title(f"Parallel runtime vs threads (n={n})")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIG / f"runtime_threads_n{n}.png", dpi=200)
    plt.close()

# Speedup for largest n
largest_n = max(r["n"] for r in rows)
omp = sorted(
    [r for r in rows if r["n"] == largest_n and r["method"] == "omp"],
    key=lambda r: r["threads"]
)
plt.figure()
threads = [r["threads"] for r in omp]
speedups = [r["speedup"] for r in omp]
plt.plot(threads, speedups, marker="o", label="Observed")
plt.plot(threads, threads, linestyle="--", label="Ideal")
plt.xlabel("Threads")
plt.ylabel("Speedup")
plt.title(f"Speedup vs threads (n={largest_n})")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(FIG / f"speedup_n{largest_n}.png", dpi=200)
plt.close()

# Efficiency for largest n
plt.figure()
plt.plot(threads, [r["efficiency"] for r in omp], marker="o")
plt.xlabel("Threads")
plt.ylabel("Efficiency")
plt.title(f"Efficiency vs threads (n={largest_n})")
plt.ylim(bottom=0)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(FIG / f"efficiency_n{largest_n}.png", dpi=200)
plt.close()

print(f"Figures saved in: {FIG}")
