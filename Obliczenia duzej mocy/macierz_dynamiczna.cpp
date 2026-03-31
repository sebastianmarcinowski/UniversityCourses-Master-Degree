#include <iostream>
#include <thread>
#include <vector>
#include <chrono>

using namespace std;

using T = float;

T **A, **B, **C;

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

    A = new T*[N];
    B = new T*[N];
    C = new T*[N];

    for (int i = 0; i < N; ++i) {
        A[i] = new T[N]();
        B[i] = new T[N]();
        C[i] = new T[N]();
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

    cout << "Pamiec dynamiczna\nLiczba watkow: " << nr_threads << "\nCzas trwania: " << elapsed_seconds.count() << " sekund\n";

    for (int i = 0; i < N; ++i) {
        delete[] A[i];
        delete[] B[i];
        delete[] C[i];
    }
    delete[] A;
    delete[] B;
    delete[] C;

    return 0;
}