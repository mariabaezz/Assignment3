import csv
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "results" / "raw_results.csv"
SUMMARY = ROOT / "results" / "summary_results.csv"

groups = defaultdict(list)

with RAW.open() as f:
    for row in csv.DictReader(f):
        key = (row["method"], int(row["n"]), int(row["threads"]))
        groups[key].append(float(row["time_s"]))

seq_median = {}
for (method, n, threads), times in groups.items():
    if method == "seq":
        seq_median[n] = statistics.median(times)

summary = []
for (method, n, threads), times in sorted(groups.items(), key=lambda x: (x[0][1], x[0][0], x[0][2])):
    med = statistics.median(times)
    q = statistics.quantiles(times, n=4, method="inclusive")
    iqr = q[2] - q[0]

    if method == "omp":
        speedup = seq_median[n] / med
        efficiency = speedup / threads
    else:
        speedup = 1.0
        efficiency = 1.0

    summary.append({
        "method": method,
        "n": n,
        "threads": threads,
        "repetitions": len(times),
        "median_time_s": med,
        "iqr_time_s": iqr,
        "speedup": speedup,
        "efficiency": efficiency,
    })

with SUMMARY.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=summary[0].keys())
    w.writeheader()
    w.writerows(summary)

print(f"Saved: {SUMMARY}")
print()
for r in summary:
    print(
        f'{r["method"]:3s} n={r["n"]:4d} p={r["threads"]:2d} '
        f'median={r["median_time_s"]:.6f}s '
        f'IQR={r["iqr_time_s"]:.6f}s '
        f'S={r["speedup"]:.3f} E={r["efficiency"]:.3f}'
    )
