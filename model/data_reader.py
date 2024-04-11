import numpy as np
import os


NO_MOVE = -1000


x = []
y = []


def read_line(string):
    values = string.split(",")
    moves_string = values[0]
    evaluations = [int(values[i]) for i in range(1, 8)]
    indexes = [0 for _ in range(7)]
    matrix = np.zeros((7, 6), dtype="int")
    turn = 1

    for move_string in moves_string:
        move = int(move_string) - 1
        matrix[move, indexes[move]] = turn
        indexes[move] += 1
        turn *= -1

    for i in range(len(evaluations)):
        if evaluations[i] == NO_MOVE:
            continue
        child_matrix = np.copy(matrix)
        child_matrix[i, indexes[i]] = turn
        x.append(child_matrix)
        y.append(evaluations[i])


cwd = os.path.realpath(__file__) + "/.."
for filename in os.listdir(cwd + "/data"):
    path = cwd + "/data/" + filename
    try:
        with open(path, "r") as file:
            for line in file:
                read_line(line.strip())
    except FileNotFoundError:
        print("File not found.")
    except IOError:
        print("Error reading the file.")

np.save(cwd + "/x.npy", x)
np.save(cwd + "/y.npy", y)
