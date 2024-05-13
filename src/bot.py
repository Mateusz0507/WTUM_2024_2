import random
import tensorflow as tf
from enums import BoardFields

import numpy as np
import numpy.typing as npt

from tkinter.filedialog import askopenfilename
from tkinter import *


class Bot:
    def __init__(self) -> None:
        self.model = None
        self.get_model()
    
    def get_model(self) -> None:
        root = Tk()
        path = askopenfilename()
        root.destroy()
        # self.model = tf.keras.models.load_model("regression/models/frail-consultancy/2024-04-10_18-33-43.keras")
        self.model = tf.keras.models.load_model(path)

    def make_move(
        self, col: int, player: int, board: npt.NDArray[np.bool_]
    ) -> npt.NDArray[np.bool_]:
        arr = board[:, col, 0] + board[:, col, 1]
        # numpy demand == comparator (`not arr`` will not work)
        row = np.argmax(arr == False)  # noqa: E712
        board[row, col, player] = True
        return np.array(board)

    def legal_moves(self, board: npt.NDArray[np.bool_]) -> list[int]:
        moves = []

        top_row = board[0, :, 0] + board[0, :, 1]
        for i in range(len(top_row)):
            # numpy demand == comparator (`not top_row[i]`` will not work)
            if top_row[i] == False:  # noqa: E712
                moves.append(i)

        return moves

    def get_bot_move(self, board: npt.NDArray[np.int8], turn: BoardFields) -> int:
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

        for col in self.legal_moves(new_board):
            test_board = self.make_move(col, turn.value - 1, new_board)
            test_board = np.expand_dims(test_board, axis=0)

            predict = self.model.predict([np.array([True]), test_board])
            predicts[col] = float(predict)

            if float(predict) > best_eval:
                best_eval = float(predict)
                best_move = col

        return best_move

    def get_random_move(self, board: npt.NDArray[np.int8], turn: BoardFields) -> int:
        board = np.rot90(board, k=1)

        new_board = np.zeros((6, 7, 2), dtype=np.bool_)
        for col in range(len(board)):
            for j in range(len(board[col])):
                if board[col][j] == 1:
                    new_board[col][j][0] = True
                if board[col][j] == 2:
                    new_board[col][j][1] = True

        return random.choice(self.legal_moves(new_board))
