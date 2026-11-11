# Assignment 3 — Parallel Matrix Multiplication

This project studies how thread count affects shared-memory matrix multiplication performance.

## Design

- Sequential baseline: reordered dense multiplication (`i-k-j`).
- Parallel implementation: same algorithm and storage, parallelised with OpenMP over matrix rows.
- Numeric type: signed 64-bit integer (`long long`).
- Input generation: deterministic pseudo-random integers in `[0, 9]`.
- Seeds: 42 for A and 4242 for B.
- Timing boundary: multiplication kernel only. Matrix allocation and input generation are outside the timer.
- Repetitions: 5 measured runs per configuration.
- Correctness: checksum equality across all configurations for each matrix size.

## macOS requirements

Install OpenMP once:

```bash
brew install libomp
```

Check CPU resources:

```bash
sysctl -n machdep.cpu.brand_string
sysctl -n hw.physicalcpu
sysctl -n hw.logicalcpu
sysctl -n hw.memsize
```

## Compile

From the project root:

```bash
clang -O2 -Xpreprocessor -fopenmp src/matrix_parallel.c \
  -I"$(brew --prefix libomp)/include" \
  -L"$(brew --prefix libomp)/lib" \
  -lomp -o run_parallel
```

## Quick correctness test

```bash
./run_parallel seq 100 1
./run_parallel omp 100 1
./run_parallel omp 100 4
```

The checksum must be identical.

## Benchmark

Edit `THREADS` in `benchmark/run_benchmark.py` so that the largest value does not exceed the number reported by:

```bash
sysctl -n hw.logicalcpu
```

Then run:

```bash
python3 benchmark/run_benchmark.py
python3 analysis/analyze.py
python3 analysis/plot_results.py
```

Outputs:

- `results/raw_results.csv`
- `results/summary_results.csv`
- figures in `figures/`

## Memory

For the final report, record peak resident memory for representative configurations with macOS `/usr/bin/time -l`, for example:

```bash
/usr/bin/time -l ./run_parallel seq 2000 1
/usr/bin/time -l ./run_parallel omp 2000 4
```

Record the `maximum resident set size` value and state that it is peak process resident memory reported by macOS `/usr/bin/time -l`.

## Metrics

For fixed matrix size `n`:

- `Tseq(n)` = median sequential runtime.
- `Tp(n)` = median parallel runtime with `p` threads.
- Speedup: `S(p) = Tseq(n) / Tp(n)`.
- Efficiency: `E(p) = S(p) / p`.

## Recommended experiment

Sizes:

```text
500, 750, 1000, 1500, 2000
```

Threads:

```text
1, 2, 4, ... up to the machine's logical processor count
```

Do not intentionally oversubscribe for the main experiment.

## Reproducibility notes to record

- Mac model / CPU model
- physical cores
- logical processors
- RAM
- macOS version
- clang version
- libomp version
- Python version
- compiler flags
- matrix sizes
- thread counts
- repetitions
