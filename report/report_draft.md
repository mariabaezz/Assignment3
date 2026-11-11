# Assignment 3 — Parallel Matrix Multiplication

## Abstract
This study investigates how thread count affects the runtime of shared-memory dense matrix multiplication. A sequential reordered `i-k-j` implementation is compared with an equivalent OpenMP implementation using the same algorithm, numeric type, storage layout and generated inputs. Runtime is measured repeatedly for several square matrix sizes and thread counts. Speedup and efficiency are calculated from median runtimes, and peak resident memory is also recorded.

## 1. Introduction and objective

### Research question
How does increasing the number of OpenMP threads affect runtime, speedup and efficiency for reordered dense matrix multiplication on the tested machine?

### Hypothesis
Parallel execution should reduce runtime for sufficiently large matrices, but speedup is expected to become sublinear as thread count increases because of thread-management overhead, memory-system limits and the serial fraction of execution.

## 2. Background
The sequential algorithm uses the loop order `i-k-j`. Its arithmetic complexity remains O(n^3). The parallel version distributes independent output rows among OpenMP threads. Since each thread writes to a different row of matrix C while matrices A and B are read-only, the chosen parallel region does not require locks for the matrix elements.

Speedup is defined as:

S(p) = Tseq(n) / Tp(n)

Efficiency is defined as:

E(p) = S(p) / p

## 3. Methodology

### 3.1 Implementations
- Sequential baseline: reordered `i-k-j`.
- Parallel: the same reordered algorithm with `#pragma omp parallel for schedule(static)` on the outer `i` loop.
- Numeric type: 64-bit signed integers.
- Storage: contiguous row-major arrays.

### 3.2 Inputs
Square matrices of sizes [INSERT FINAL SIZES].
Values are integers in [0, 9], generated deterministically with fixed seeds.
Input allocation and generation occur outside the timed multiplication region.

### 3.3 Environment
- CPU:
- Physical cores:
- Logical processors:
- RAM:
- Operating system:
- Compiler:
- Compiler flags:
- OpenMP runtime:
- Python:

### 3.4 Measurement protocol
Each configuration is measured five times. Runtime is measured with a monotonic clock around the multiplication kernel only. The median is used as the central statistic and the interquartile range (IQR) as the variability measure.

The parallel version is measured with one thread as well as higher supported thread counts. This makes the framework overhead visible.

Correctness is checked by requiring identical result checksums for all implementations and thread counts for each matrix size.

Peak resident memory is measured with macOS `/usr/bin/time -l`.

## 4. Results

### 4.1 Runtime
[INSERT TABLE / FIGURE]

### 4.2 Speedup
[INSERT FIGURE]

### 4.3 Efficiency
[INSERT FIGURE]

### 4.4 Memory
[INSERT MEMORY TABLE]

## 5. Discussion
Discuss:
- whether parallelism helps more for larger matrices;
- the difference between sequential baseline and OpenMP with one thread;
- where speedup begins to flatten;
- whether efficiency falls as p increases;
- physical cores vs logical processors;
- memory-system and scheduling overhead;
- any anomalous run using the raw measurements and IQR;
- limitations of a single-machine experiment.

Do not claim that OpenMP or C is universally faster. Conclusions apply only to the tested implementation, machine, inputs and compiler settings.

## 6. Conclusions
Answer the research question directly using the measured data. State the best tested thread count for the larger matrices and the corresponding observed speedup and efficiency. Mention that parallel execution is not automatically advantageous for small workloads if the measurements show this.

## References and materials
[Add OpenMP reference and repository link.]
