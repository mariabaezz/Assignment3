import csv
import os
import platform
import re
import statistics
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXE = ROOT / "run_parallel"
OUT = ROOT / "results" / "raw_results.csv"

SIZES = [500, 750, 1000, 1500, 2000]
THREADS = [1, 2, 4, 8]   # Edit after checking your Mac's logical CPUs.
REPETITIONS = 5

LINE_RE = re.compile(
    r"method=(?P<method>\w+),n=(?P<n>\d+),threads=(?P<threads>\d+),"
    r"time=(?P<time>[0-9.]+),checksum=(?P<checksum>\d+)"
)

def run_one(method, n, threads):
    p = subprocess.run(
        [str(EXE), method, str(n), str(threads)],
        check=True, capture_output=True, text=True
    )
    line = p.stdout.strip().splitlines()[-1]
    m = LINE_RE.fullmatch(line)
    if not m:
        raise RuntimeError(f"Unexpected output: {line}")
    d = m.groupdict()
    return {
        "method": d["method"],
        "n": int(d["n"]),
        "threads": int(d["threads"]),
        "time_s": float(d["time"]),
        "checksum": int(d["checksum"]),
    }

def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows = []

    for n in SIZES:
        # Sequential baseline: same algorithm, no OpenMP region.
        for rep in range(1, REPETITIONS + 1):
            r = run_one("seq", n, 1)
            r["repetition"] = rep
            rows.append(r)
            print(r)

        # Parallel implementation, including p=1 to expose OpenMP overhead.
        for threads in THREADS:
            for rep in range(1, REPETITIONS + 1):
                r = run_one("omp", n, threads)
                r["repetition"] = rep
                rows.append(r)
                print(r)

    # Verify that all configurations for a given n produce the same checksum.
    for n in SIZES:
        checks = {r["checksum"] for r in rows if r["n"] == n}
        if len(checks) != 1:
            raise RuntimeError(f"Correctness failure for n={n}: checksums={checks}")

    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["method", "n", "threads", "repetition", "time_s", "checksum"]
        )
        w.writeheader()
        w.writerows(rows)

    print(f"\nSaved: {OUT}")

if __name__ == "__main__":
    main()
