#include <iostream>
#include <thread>
#include <vector>
#include <chrono>

using namespace std;

using T = float;

int N = 2560;
int nr_threads = 1;
T **A,**B,**C;
T *a,*b,*c;

void func(int tid, int current_threads) {
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
	N = stoi(argv[1]);
    nr_threads = stoi(argv[2]);

	A = new T*[N]();
	B = new T*[N]();
	C = new T*[N]();

    a = new T[N*N]();
    b = new T[N*N]();
    c = new T[N*N]();

    for (int i=0; i<N; ++i) {
        A[i] = a+i*N;
        B[i] = b+i*N;
        C[i] = c+i*N;
    }

    std::vector<std::thread> th;

    const auto start{std::chrono::steady_clock::now()};

    for (int i = 0; i < nr_threads; ++i) {
        th.push_back(std::thread(func, i, nr_threads));
    }

    for(auto &t: th){
        t.join();
    }

    const auto finish{std::chrono::steady_clock::now()};
    const std::chrono::duration<double> elapsed_seconds{finish - start};

    cout << "Liczba wątków: " << nr_threads << "\nCzas trwania: " << elapsed_seconds.count() << " sekund\n";

    delete []A;
    delete []B;
    delete []C;
    delete []a;
    delete []b;
    delete []c;
}
