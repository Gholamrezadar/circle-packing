#!/bin/bash

# Compile the program
echo "Compiling the program..."
g++ -Wall -O3 -std=c++17 circle_packing.cpp -o circle_packing
echo -e "Done!\n"

# Run the program
echo "Running the program..."
time ./circle_packing > result.txt
echo -e "Done!\n"

# Plot the result
echo "Plotting..."
time python3.11 plot_circle_data.py
