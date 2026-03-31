cmake_minimum_required(VERSION 4.1)
project(Obliczenia_duzej_mocy)

set(CMAKE_CXX_STANDARD 14)

add_executable(Obliczenia_duzej_mocy
        macierz_statyczna.cpp
        macierz_dynamiczna_liniowa.cpp
        macierz_dynamiczna.cpp
        macierz_alloc.cpp
)
