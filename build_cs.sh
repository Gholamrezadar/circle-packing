#!/bin/bash

# Compile the program
echo "Compiling the program..."
g++ -Wall -O3 -std=c++17 circle_packing.cpp -o circle_packing
echo -e "Done!\n"

# Run the program
echo "Running the program..."
time ./circle_packing > result_codespaces.txt
echo -e "Done!\n"

# Plot the result
echo "Plotting..."
time python3 plot_circle_data_opencv.py

