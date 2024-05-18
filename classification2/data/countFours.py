import base64
import numpy as np
import pandas as pd

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

def calculate_line_score2(line):
    player1_count = sum(1 for disk in line if disk[0])  # Count of Player 1's disks
    player2_count = sum(1 for disk in line if disk[1])  # Count of Player 2's disks

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

def generate_output_matrix2(board):
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
            output_matrix[index] = calculate_line_score2(line)
    # Check vertical lines
    for i in range(rows - 3):
        for j in range(cols):
            line[0]=board[i,j]
            line[1]=board[i+1,j]
            line[2]=board[i+2,j]
            line[3]=board[i+3,j]
            index = k
            k=k+1
            output_matrix[index] = calculate_line_score2(line)
    # Check diagonal lines (\)
    for i in range(rows - 3):
        for j in range(cols - 3):
            line[0]=board[i,j]
            line[1]=board[i+1,j+1]
            line[2]=board[i+2,j+2]
            line[3]=board[i+3,j+3]
            index = k
            k=k+1
            output_matrix[index] = calculate_line_score2(line)
    # Check diagonal lines (/)
    for i in range(rows - 3):
        for j in range(3, cols):
            line[0]=board[i,j]
            line[1]=board[i+1,j-1]
            line[2]=board[i+2,j-2]
            line[3]=board[i+3,j-3]
            index = k
            k=k+1
            output_matrix[index] = calculate_line_score2(line)
    return output_matrix

data = pd.read_csv("data/csv/parsed_data_1.csv")
array_data_full = np.array([np.frombuffer(base64.b64decode(board), dtype=np.bool_).reshape((6,7,2)) for board in data["board"]])
#fours_data_full = np.array([generate_output_matrix(array_data_full[i]) for i in range(len(array_data_full))])
#array_data_full = np.array([np.frombuffer(base64.b64decode(data["board"][i]), dtype=np.bool_).reshape((6,7,2)) for i in range(2)])
#array_data_full = np.array(np.frombuffer(base64.b64decode(data["board"][15]), dtype=np.bool_).reshape((6,7,2)))
#print(array_data_full)
# Generate the output matrix
output_matrix = generate_output_matrix(array_data_full[0])
print(output_matrix)
outputmatrix2=generate_output_matrix2(array_data_full[0])
print(outputmatrix2)
