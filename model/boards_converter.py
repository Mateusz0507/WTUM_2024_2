import numpy as np
import os


cwd = os.path.realpath(__file__) + "/.."
boards = np.load(cwd + "/boards.npy")
x = []


def convert_board(board):
    # TODO make function
    result = None
    x.append(result)


for board in boards:
    convert_board(board)

np.save(cwd + "/x.npy", x)
