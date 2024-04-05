import base64
import csv
import numpy as np
import pandas as pd
import numpy.typing as npt

df = pd.read_csv("data/data5.csv", dtype=str)

shape = (6, 7, 2)


def make_move(col: int, player: int, board: npt.NDArray[np.bool_]) -> None:
    arr1 = board[:, col, 0][::-1]
    arr2 = board[:, col, 1][::-1]
    arr = arr1 + arr2
    row = np.argmax(arr == False)
    board[5 - row, col, player] = True


rows = []

for i in range(df.shape[0]):
    moves = str(df["moves"][i])
    if moves == "nan":
        moves = ""

    board = np.zeros(shape, dtype=np.bool_)
    player = 0

    for j in range(len(moves)):
        make_move(int(moves[j]) - 1, player, board)
        player = 1 if player == 0 else 0

    binary_board = board.tobytes()
    base64data = base64.b64encode(binary_board).decode()

    max_eval = max([int(df[f"c{j}"][i]) for j in range(7)])
    if max_eval == -1000:
        continue

    rows.append([base64data, max_eval])


with open("data/parsed_data5.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)
