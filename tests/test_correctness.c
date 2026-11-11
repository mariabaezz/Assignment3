#define main original_benchmark_main
#include "../src/matrix_parallel.c"
#undef main
#include <stdio.h>

static int check_case(const char *name, const long long *A, const long long *B,
                      const long long *expected, int n) {
    long long *seq = alloc_matrix(n);
    long long *par = alloc_matrix(n);
    if (!seq || !par) { free(seq); free(par); return 1; }
    multiply_reordered_seq(A, B, seq, n);
    int errors = !matrices_equal(seq, expected, n);
    for (int p = 1; p <= 8; p *= 2) {
        multiply_reordered_omp(A, B, par, n, p);
        if (!matrices_equal(par, expected, n)) errors = 1;
    }
    printf("%s: %s\n", name, errors ? "FAIL" : "PASS");
    free(seq); free(par);
    return errors;
}

int main(void) {
    const long long A[] = {1,2,3,4};
    const long long B[] = {5,6,7,8};
    const long long AB[] = {19,22,43,50};
    const long long I[] = {1,0,0,1};
    const long long Z[] = {0,0,0,0};
    int errors = 0;
    errors += check_case("Known 2x2 product", A, B, AB, 2);
    errors += check_case("Identity", A, I, A, 2);
    errors += check_case("Zero", A, Z, Z, 2);
    return errors ? 1 : 0;
}
