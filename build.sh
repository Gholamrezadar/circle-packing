#!/bin/bash

# Compile the program
g++ -Wall -O3 -std=c++17 circle_packing.cpp -o circle_packing

# Run the program
./circle_packing > result.txt

# Plot the result
python3.11 load_cpp_data.py
