import random
import tensorflow as tf
from enums import BoardFields

import numpy as np
import numpy.typing as npt

# TODO: maybe select model from GUI?
model = tf.keras.models.load_model(
    "regression/models/frail-consultancy/2024-04-10_18-33-43.keras"
)


def make_move(
    col: int, player: int, board: npt.NDArray[np.bool_]
) -> npt.NDArray[np.bool_]:
    arr = board[:, col, 0] + board[:, col, 1]
    # numpy demand == comparator (`not arr`` will not work)
    row = np.argmax(arr == False)  # noqa: E712
    board[row, col, player] = True
    return np.array(board)


def legal_moves(board: npt.NDArray[np.bool_]) -> list[int]:
    moves = []

    top_row = board[0, :, 0] + board[0, :, 1]
    for i in range(len(top_row)):
        # numpy demand == comparator (`not top_row[i]`` will not work)
        if top_row[i] == False:  # noqa: E712
            moves.append(i)

    return moves


def get_bot_move(board: npt.NDArray[np.int8], turn: BoardFields) -> int:
    board = np.rot90(board, k=1)

    new_board = np.zeros((6, 7, 2), dtype=np.bool_)
    for col in range(len(board)):
        for j in range(len(board[col])):
            if board[col][j] == 1:
                new_board[col][j][0] = True
            if board[col][j] == 2:
                new_board[col][j][1] = True

    best_move = -1
    best_eval = -np.Infinity
    predicts = [-1000.0 for _ in range(7)]

    for col in legal_moves(new_board):
        test_board = make_move(col, turn.value - 1, new_board)
        test_board = np.expand_dims(test_board, axis=0)

        predict = model.predict([np.array([True]), test_board])
        predicts[col] = float(predict)

        if float(predict) > best_eval:
            best_eval = float(predict)
            best_move = col

    return best_move


def get_random_move(board: npt.NDArray[np.int8], turn: BoardFields) -> int:
    board = np.rot90(board, k=1)

    new_board = np.zeros((6, 7, 2), dtype=np.bool_)
    for col in range(len(board)):
        for j in range(len(board[col])):
            if board[col][j] == 1:
                new_board[col][j][0] = True
            if board[col][j] == 2:
                new_board[col][j][1] = True

    return random.choice(legal_moves(new_board))
