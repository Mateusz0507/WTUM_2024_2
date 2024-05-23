import random
import tensorflow as tf
from enums import BoardFields
from convert_board import convert_board

import numpy as np
import numpy.typing as npt

from tkinter.filedialog import askopenfilename
from tkinter import *

BOARD_ROWS = 6
BOARD_COLUMNS = 7


class Bot:
    def __init__(self) -> None:
        self.model = None
        self.get_model()
    
    def get_model(self) -> None:
        root = Tk()
        path = askopenfilename()
        root.destroy()
        self.model = tf.keras.models.load_model(path)

    def legal_moves(self, board: npt.NDArray[np.int8]) -> list[int]:
        moves = []
        for i in range(BOARD_COLUMNS):
            if board[i, BOARD_ROWS - 1] == BoardFields.EMPTY.value:
                moves.append(i)

        return moves
    
    def get_bot_move(self, board: npt.NDArray[np.int8], turn: BoardFields) -> int:
        if (self.model.layers[0].name in ["regression: board and lines", "regression: lines", "regression: proof of concept"]):
            return self.get_bot_move_regression2(board, turn)
        else:
            return self.get_bot_move_regression(board, turn)
    

    def get_bot_move_regression2(self, board: npt.NDArray[np.int8], turn: BoardFields) -> int:
        best_move = -1
        best_eval = np.Infinity
        predicts = [-1000.0 for _ in range(7)]

        for col in self.legal_moves(board):
            changed_board = board.copy()
            board_column = changed_board[col]
            row = (np.where(board_column == BoardFields.EMPTY.value)[0])[0]
            changed_board[col, row] = turn.value
            converted_board = convert_board(changed_board.copy())

            match self.model.layers[0].name:
                case "regression: board and lines":
                    input = [np.array([converted_board[0]]), np.array([converted_board[1]]), np.array([converted_board[2]])]
                case "regression: lines":
                    input = [np.array([converted_board[1]]), np.array([converted_board[2]])]
                case "regression: proof of concept":
                    input = [np.array([converted_board[1]]), np.array([converted_board[2]])]
                case _:
                    raise Exception("Invalid model type: ", self.model.layers[0].name)

            predict = self.model.predict(input)
            predicts[col] = float(predict)
            if float(predict) < best_eval:
                best_eval = float(predict)
                best_move = col

        print(predicts)

        return best_move


    def convert_board_regression(self, board: npt.NDArray[np.int8]):
        board = np.rot90(board, k=1)

        new_board = np.zeros((6, 7, 2), dtype=np.bool_)
        for col in range(len(board)):
            for j in range(len(board[col])):
                if board[col][j] == 1:
                    new_board[col][j][0] = True
                if board[col][j] == 2:
                    new_board[col][j][1] = True
        new_board = np.expand_dims(new_board, axis=0)
        return [np.array([True]), new_board]
    
    def get_bot_move_regression(self, board: npt.NDArray[np.int8], turn: BoardFields) -> int:
        best_move = -1
        best_eval = np.Infinity
        predicts = [-1000.0 for _ in range(7)]

        for col in self.legal_moves(board):
            changed_board = board.copy()
            changed_board[col, BOARD_ROWS - 1] = turn.value

            converted_board = self.convert_board_regression(changed_board.copy())
            predict = self.model.predict(converted_board)
            predicts[col] = float(predict)

            if float(predict) < best_eval:
                best_eval = float(predict)
                best_move = col

        return best_move


    def get_bot_move_classification(self, board: npt.NDArray[np.int8], turn: BoardFields) -> int:
      board = np.rot90(board, k=1)
      new_board = np.zeros((6, 7, 2), dtype=np.bool_)
      for col in range(len(board)):
          for j in range(len(board[col])):
              if board[col][j] == 1:
                  new_board[col][j][0] = True
              if board[col][j] == 2:
                  new_board[col][j][1] = True
      predicts = self.model.predict([np.array([0]),new_board[None]])
      best_index = self.legal_moves(new_board)[0]
      for col in self.legal_moves(new_board):
          if(predicts[0][best_index]<predicts[0][col]):
              best_index=col
      return best_index
    
    def get_bot_move_classification2(self, board: npt.NDArray[np.int8], turn: BoardFields) -> int:
        board = np.rot90(board, k=1)

        new_board = np.zeros((6, 7, 2), dtype=np.bool_)
        for col in range(len(board)):
            for j in range(len(board[col])):
                if board[col][j] == 1:
                    new_board[col][j][0] = True
                if board[col][j] == 2:
                    new_board[col][j][1] = True
        fours_matrix = generate_output_matrix(new_board)
        predicts = self.model.predict([np.array([0]),new_board[None],fours_matrix[None]])
        best_index=self.legal_moves(new_board)[0]
        for col in self.legal_moves(new_board):
            if(predicts[0][best_index]<predicts[0][col]):
                best_index=col
        return best_index


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

def calculate_line_score(line):
    player1_count = np.sum(line[:,0] == True)  # Count of Player 1's disks
    player2_count = np.sum(line[:,1] == True)  # Count of Player 2's disks

    if player2_count == 3 and player1_count == 0:
        return -3
    elif player2_count == 2 and player1_count == 0:
        return -2
    elif player2_count == 1 and player1_count == 0:
        return -1
    elif player1_count > 0 and player2_count > 0:
        return 0
    elif player2_count == 0 and player1_count == 1:
        return 1
    elif player2_count == 0 and player1_count == 2:
        return 2
    elif player2_count == 0 and player1_count == 3:
        return 3
    else:
        return 0

def generate_output_matrix(board):
    rows, cols, _ = board.shape
    output_matrix = np.zeros((69, 1), dtype=np.int8)
    k=0
    # Check horizontal lines
    for i in range(rows):
        for j in range(cols - 3):
            line = board[i, j:j+4, :]
            index = k
            k=k+1
            output_matrix[index] = calculate_line_score(line)
    # Check vertical lines
    for i in range(rows - 3):
        for j in range(cols):
            line = board[i:i+4, j, :]
            index = k
            k=k+1
            output_matrix[index] = calculate_line_score(line)
    # Check diagonal lines (\)
    for i in range(rows - 3):
        for j in range(cols - 3):
            line = board[i:i+4, j:j+4, :]
            index = k
            k=k+1
            output_matrix[index] = calculate_line_score(line.diagonal().transpose())
    # Check diagonal lines (/)
    for i in range(rows - 3):
        for j in range(3, cols):
            line = board[i:i+4, j-3:j+1, :]
            index = k
            k=k+1
            output_matrix[index] = calculate_line_score(np.fliplr(line).diagonal().transpose())
    return output_matrix