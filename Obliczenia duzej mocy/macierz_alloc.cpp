#include <iostream>
#include <thread>
#include <vector>
#include <chrono>
#include <cstdlib>
#include <cstring>

using namespace std;

using T = float;

T **A, **B, **C;
T *a, *b, *c;

void func(int tid, int current_threads, int N) {
    int lb = tid * (N / current_threads);
    int ub = lb + (N / current_threads) - 1;

    for (int i = lb; i <= ub; ++i) {
        for (int j = 0; j < N; ++j) {
            for (int k = 0; k < N; ++k) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

int main(int argc, char const *argv[]) {
    if (argc < 3) return 1;
    int N = stoi(argv[1]);
    int nr_threads = stoi(argv[2]);

    size_t alignment = 64;
    size_t size = N * N * sizeof(T);
    size_t alloc_size = (size + alignment - 1) & ~(alignment - 1);

    A = new T*[N];
    B = new T*[N];
    C = new T*[N];

    a = static_cast<T*>(std::aligned_alloc(alignment, alloc_size));
    b = static_cast<T*>(std::aligned_alloc(alignment, alloc_size));
    c = static_cast<T*>(std::aligned_alloc(alignment, alloc_size));

    std::memset(a, 0, alloc_size);
    std::memset(b, 0, alloc_size);
    std::memset(c, 0, alloc_size);

    for (int i = 0; i < N; ++i) {
        A[i] = a + i * N;
        B[i] = b + i * N;
        C[i] = c + i * N;
    }

    std::vector<std::thread> th;
    const auto start = std::chrono::steady_clock::now();

    for (int i = 0; i < nr_threads; ++i) {
        th.push_back(std::thread(func, i, nr_threads, N));
    }

    for(auto &t: th){
        t.join();
    }

    const auto finish = std::chrono::steady_clock::now();
    std::chrono::duration<double> elapsed_seconds = finish - start;

    cout << "Pamiec aligned_alloc\nLiczba watkow: " << nr_threads << "\nCzas trwania: " << elapsed_seconds.count() << " sekund\n";

    delete[] A;
    delete[] B;
    delete[] C;
    std::free(a);
    std::free(b);
    std::free(c);

    return 0;
}