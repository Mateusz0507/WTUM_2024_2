import base64
import csv
import numpy as np
import pandas as pd
import numpy.typing as npt
import time
def XDfunc(paths,outputPath):
    arrayDaya = []
    targetData=[]
    numberData=[]
    for path in paths:
        df = pd.read_csv(path+".csv", dtype=str)
        shape = (6, 7, 2)
        def make_move(col: int, player: int, board: npt.NDArray[np.bool_]) -> None:
            arr1 = board[:, col, 0][::-1]
            arr2 = board[:, col, 1][::-1]
            arr = arr1 + arr2
            row = np.argmax(arr == False)
            board[5 - row, col, player] = True

        for i in range(df.shape[0]):
            moves = str(df["moves"][i])
            if moves == "nan":
                moves = ""

            board = np.zeros(shape, dtype=np.bool_)
            player = 0

            for j in range(len(moves)):
                make_move(int(moves[j]) - 1, player, board)
                player = 1 if player == 0 else 0


            max_eval = max([int(df[f"c{j}"][i]) for j in range(7)])
            if max_eval == -1000:
                continue
            eval=[]
            for k in range(7):
                eval.append(int(df[f"c{k}"][i]))
            arrayDaya.append(board)
            targetData.append(eval)
            numberData.append(len(moves)%2)
    np.save(outputPath+"arrayData.npy", np.array(arrayDaya,dtype=bool))
    np.save(outputPath+"numberData.npy", np.array(numberData))
    np.save(outputPath+"targetData.npy", np.array(targetData))

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
    line=[[False,False],[False,False],[False,False],[False,False]]
    # Check horizontal lines
    for i in range(rows):
        for j in range(cols - 3):
            line[0]=board[i,j]
            line[1]=board[i,j+1]
            line[2]=board[i,j+2]
            line[3]=board[i,j+3]
            index = k
            k=k+1
            output_matrix[index] = calculate_line_score(line)
    # Check vertical lines
    for i in range(rows - 3):
        for j in range(cols):
            line[0]=board[i,j]
            line[1]=board[i+1,j]
            line[2]=board[i+2,j]
            line[3]=board[i+3,j]
            index = k
            k=k+1
            output_matrix[index] = calculate_line_score(line)
    # Check diagonal lines (\)
    for i in range(rows - 3):
        for j in range(cols - 3):
            line[0]=board[i,j]
            line[1]=board[i+1,j+1]
            line[2]=board[i+2,j+2]
            line[3]=board[i+3,j+3]
            index = k
            k=k+1
            output_matrix[index] = calculate_line_score(line)
    # Check diagonal lines (/)
    for i in range(rows - 3):
        for j in range(3, cols):
            line[0]=board[i,j]
            line[1]=board[i+1,j-1]
            line[2]=board[i+2,j-2]
            line[3]=board[i+3,j-3]
            index = k
            k=k+1
            output_matrix[index] = calculate_line_score(line)
    return output_matrix
def generate_and_save_all_output_matrix(boards,outputPath):
    output_matrix=[]
    for board in boards:
        start=time.time()
        output_matrix.append(np.array(generate_output_matrix(board)))
        end=time.time()
        duration=(end-start)
    np.save(outputPath+"foursInRow.npy", np.array(output_matrix))

    