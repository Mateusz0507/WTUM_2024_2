import numpy as np
from enum import Enum

class BoardFields(Enum):
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2

def every_line_of_4():
    indexes_of_every_line_of_4 = []

    # Horizontal _
    for column in range(7 - 3):
        for row in range(6):
            columns_indexes = [column + i for i in range(4)]
            row_indexes = [row for _ in range(4)]
            indexes_of_every_line_of_4.append([columns_indexes, row_indexes])

    # Vertical |
    for column in range(7):
        for row in range(6 - 3):
            columns_indexes = [column for _ in range(4)]
            row_indexes = [row + i for i in range(4)]
            indexes_of_every_line_of_4.append([columns_indexes, row_indexes])

    # Diagonal /
    for column in range(7 - 3):
        for row in range(6 - 3):
            columns_indexes = [column + i for i in range(4)]
            row_indexes = [row + i for i in range(4)]
            indexes_of_every_line_of_4.append([columns_indexes, row_indexes])

    # Diagonal \
    for column in range(3, 7):
        for row in range(6 - 3):
            columns_indexes = [column - i for i in range(4)]
            row_indexes = [row + i for i in range(4)]
            indexes_of_every_line_of_4.append([columns_indexes, row_indexes])
    
    return indexes_of_every_line_of_4


def convert_board(board):
    board_reshaped = np.zeros((2, 7, 6), dtype=bool)
    board_reshaped[0, :, :] = (board == BoardFields.PLAYER1.value)
    board_reshaped[1, :, :] = (board == BoardFields.PLAYER2.value)

    # Result is set of two arrays (for player and opponent) that counts number of lines of 1, 2 and 3
    player_lines = [0, 0, 0]
    opponent_lines = [0, 0, 0]

    indexes_of_every_line_of_4 = every_line_of_4()

    for indexes_of_line_of_4 in indexes_of_every_line_of_4:
        line_of_4 = board[indexes_of_line_of_4[0], indexes_of_line_of_4[1]]

        # For player
        if BoardFields.PLAYER2.value not in line_of_4:
            number_of_discs = np.sum(line_of_4 == BoardFields.PLAYER1.value)
            if 0 < number_of_discs < 4:
                player_lines[number_of_discs - 1] += 1

        # For oponent
        if BoardFields.PLAYER1.value not in line_of_4:
            number_of_discs = np.sum(line_of_4 == BoardFields.PLAYER2.value)
            if 0 < number_of_discs < 4:
                opponent_lines[number_of_discs - 1] += 1
    
    result = [board_reshaped, player_lines, opponent_lines]
    return result
