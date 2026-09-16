"""
Programming Language: Python 3
IDE Used: Pycharm

Compilation & Execution:
To run this program, save it as I3.py and execute with:
> python I3.py

Author: Curtis Been
Date: April 18th 2025
Class: CS 4500
Project: Individual Project 3 (I3)

Description:
This program reads a user-specified .csv file containing a matrix of non-negative integers (max 10x10),
verifies its format, and performs a series of matrix operations:
1. Transposes the matrix and writes it to Transposed.csv
2. Generates a presence matrix (1s for non-zero, 0s for zeros) and writes to Presence.csv
3. Reads M1.csv and M2.csv, adds them, and writes the result to M1plusM2.csv
4. Compares M1 and M2 element-wise and writes 0/1/2 to WhichBigger.csv depending on equality/greater/less

External Files Used:
- User-provided: *.csv input matrix file, M1.csv, M2.csv
- Program-generated: Transposed.csv, Presence.csv, M1plusM2.csv, WhichBigger.csv

Outside Resources:
- Python documentation for file I/O and CSV module
- StackOverflow for transposing and checking file extensions

"""

import os
import csv


def pause(msg="Press ENTER to continue..."):
    input(msg)


def display_intro():
    print("This program reads a matrix from a .CSV file and performs the following:")
    print("- Transposes the matrix and writes to Transposed.csv")
    print("- Writes a presence matrix to Presence.csv (1 = non-zero, 0 = zero)")
    print("- Reads M1.csv and M2.csv, adds them, writes to M1plusM2.csv")
    print("- Compares M1 and M2 values and writes 0/1/2 to WhichBigger.csv")
    pause()


def get_valid_filename():
    while True:
        filename = input("Enter the name of a .CSV file (e.g., data.csv): ").strip()
        if not filename.lower().endswith('.csv'):
            print("Error: File must end with .csv")
            continue
        if not os.path.exists(filename):
            print("Error: File does not exist in current directory.")
            continue
        return filename


def read_matrix(filename):
    with open(filename, 'r', newline='') as f:
        reader = csv.reader(f)
        matrix = [list(map(int, row)) for row in reader]

    row_lengths = [len(row) for row in matrix]
    if not all(length == row_lengths[0] for length in row_lengths):
        print("Error: CSV file contains rows with inconsistent number of columns.")
        pause("Press ENTER to exit...")
        exit(1)

    if len(matrix) > 10 or len(matrix[0]) > 10:
        print("Error: Matrix dimensions exceed 10x10.")
        pause("Press ENTER to exit...")
        exit(1)

    return matrix


def write_matrix(filename, matrix):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(matrix)



def transpose_matrix(matrix):
    return [list(row) for row in zip(*matrix)]


def presence_matrix(matrix):
    return [[1 if val != 0 else 0 for val in row] for row in matrix]


def matrix_add(m1, m2):
    return [[m1[i][j] + m2[i][j] for j in range(len(m1[0]))] for i in range(len(m1))]


def which_bigger(m1, m2):
    result = []
    for i in range(len(m1)):
        row = []
        for j in range(len(m1[0])):
            if m1[i][j] == m2[i][j]:
                row.append(0)
            elif m1[i][j] > m2[i][j]:
                row.append(1)
            else:
                row.append(2)
        result.append(row)
    return result


def main():
    display_intro()

    input_file = get_valid_filename()
    matrix = read_matrix(input_file)

    # Transpose and write
    transposed = transpose_matrix(matrix)
    write_matrix("Transposed.csv", transposed)

    # Presence matrix
    presence = presence_matrix(matrix)
    write_matrix("Presence.csv", presence)

    # Read and add M1, M2
    try:
        m1 = read_matrix("M1.csv")
        m2 = read_matrix("M2.csv")
        if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
            raise ValueError("M1 and M2 are not the same shape.")
    except Exception as e:
        print("Error reading M1.csv or M2.csv:", e)
        pause("Press ENTER to exit...")
        exit(1)

    added = matrix_add(m1, m2)
    write_matrix("M1plusM2.csv", added)

    compare = which_bigger(m1, m2)
    write_matrix("WhichBigger.csv", compare)

    print("\nAll files written successfully.")
    pause("Press ENTER to exit...")


if __name__ == "__main__":
    main()
