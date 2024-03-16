from enum import Enum
import pygame as pg
import numpy as np
from colors import *


class BoardFields(Enum):
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2

class GameResult(Enum):
    NO_RESULT = -1
    TIE = 0
    PLAYER1_WIN = 1
    PLAYER2_WIN = 2


# Parameters
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
POKE_RADIUS = min(WINDOW_WIDTH / 20, WINDOW_HEIGHT / 20)

BACKGROUND_COLOR = BLACK
TEXT_COLOR = WHITE
BOARD_COLOR = BLUE
PLAYER1_COLOR = YELLOW
PLAYER2_COLOR = RED


# Constants
BOARD_ROWS = 6
BOARD_COLUMNS = 7
GAP = POKE_RADIUS / 2
BOARD_LEFT_BOUNDARY = WINDOW_WIDTH / 2 - (7 * POKE_RADIUS + 4 * GAP)
BOARD_WIDTH = 14 * POKE_RADIUS + 8 * GAP
BOARD_RIGHT_BOUNDARY = BOARD_LEFT_BOUNDARY + BOARD_WIDTH
BOARD_TOP_BOUNDARY = WINDOW_HEIGHT / 2 - (6 * POKE_RADIUS + 3.5 * GAP) + (2 * POKE_RADIUS + GAP) / 2
BOARD_HEIGHT = 12 * POKE_RADIUS + 7 * GAP
BOARD_BOTTOM_BOUNDARY = BOARD_TOP_BOUNDARY + BOARD_HEIGHT
HEIGHT_ABOVE_BOARD = BOARD_TOP_BOUNDARY - (GAP + POKE_RADIUS)


pg.init()
WINDOW = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("Connect Four")


class Game:
    def __init__(self):
        self.initialize()

    def initialize(self):
        self.board = np.array([[BoardFields.EMPTY.value for rows in range(BOARD_ROWS)] for columns in range(BOARD_COLUMNS)], dtype="int8")
        self.turn = BoardFields.PLAYER1.value
        self.result = GameResult.NO_RESULT
        self.selected_column = 0 # unimportant init value
 
    def make_move(self):
        for row in range(BOARD_ROWS):
            if self.board[self.selected_column, row] == BoardFields.EMPTY.value:
                self.board[self.selected_column, row] = self.turn
                self.turn = BoardFields.PLAYER1.value if self.turn == BoardFields.PLAYER2.value else BoardFields.PLAYER2.value
                break
 
    def is_mouse_above_board(self, mouse_x):
        return BOARD_LEFT_BOUNDARY + GAP / 2 < mouse_x < BOARD_RIGHT_BOUNDARY - GAP / 2
        
    def check_if_end(self):
        if self.check_if_player_won(BoardFields.PLAYER1.value):
            self.result = GameResult.PLAYER1_WIN
        elif self.check_if_player_won(BoardFields.PLAYER2.value):
            self.result = GameResult.PLAYER2_WIN
        elif np.count_nonzero(self.board == BoardFields.EMPTY.value) == 0:
            self.result = GameResult.TIE

        x = 123
 
    def check_if_player_won(self, player):
        # HORIZONTAL _
        for i in range(6):
            for j in range(4):
                if (
                    np.count_nonzero(self.board[[j, j + 1, j + 2, j + 3], i] == player)
                    == 4
                ):
                    return True
        # VERTICAL |
        for i in range(3):
            for j in range(7):
                if (
                    np.count_nonzero(self.board[j, [i, i + 1, i + 2, i + 3]] == player)
                    == 4
                ):
                    return True
        # DIAGONAL \
        for i in range(3):
            for j in range(4):
                if (
                    np.count_nonzero(
                        self.board[[j, j + 1, j + 2, j + 3], [i, i + 1, i + 2, i + 3]]
                        == player
                    )
                    == 4
                ):
                    return True
        # DIAGONAL /
        for i in range(3):
            for j in range(3, 7):
                if (
                    np.count_nonzero(
                        self.board[[j, j - 1, j - 2, j - 3], [i, i + 1, i + 2, i + 3]]
                        == player
                    )
                    == 4
                ):
                    return True
 
        return False
 
    def end(self):
        WINDOW.fill(BACKGROUND_COLOR)
        self.draw_board()
        if self.result == GameResult.PLAYER1_WIN:
            message = "PLAYER 1 WON"
            color = PLAYER1_COLOR
        elif self.result == GameResult.PLAYER2_WIN:
            message = "PLAYER 2 WON"
            color = PLAYER2_COLOR
        elif self.result == GameResult.TIE:
            message = "DRAW"
            color = TEXT_COLOR
        else:
            raise Exception("Invalid result value: ", self.result)
 
        text = pg.font.Font(None, int(2 * POKE_RADIUS)).render(message, True, color)
        text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, HEIGHT_ABOVE_BOARD))
        WINDOW.blit(text, text_rect)
        pg.display.update()
 
    def draw(self, mouse_x):
        WINDOW.fill(BACKGROUND_COLOR)
        self.draw_board()
        if (self.is_mouse_above_board(mouse_x)):
            self.draw_puck(mouse_x)
        pg.display.update()
 
    def draw_board(self):
        pg.draw.rect(WINDOW, BOARD_COLOR, [BOARD_LEFT_BOUNDARY, BOARD_TOP_BOUNDARY, BOARD_WIDTH, BOARD_HEIGHT])
        for column in range(BOARD_COLUMNS):
            for row in range(BOARD_ROWS):
                if self.board[column, row] == BoardFields.EMPTY.value:
                    color = BACKGROUND_COLOR
                elif self.board[column, row] == BoardFields.PLAYER1.value:
                    color = PLAYER1_COLOR
                elif self.board[column, row] == BoardFields.PLAYER2.value:
                    color = PLAYER2_COLOR
                else:
                    raise Exception("Invalid color value: ", self.color)

                pg.draw.circle(WINDOW, color, [
                        BOARD_LEFT_BOUNDARY + (POKE_RADIUS + GAP) + column * (2 * POKE_RADIUS + GAP),
                        BOARD_BOTTOM_BOUNDARY - (POKE_RADIUS + GAP) - row * (2 * POKE_RADIUS + GAP),
                    ], POKE_RADIUS)
 
    def draw_puck(self, mouse_x):
        if self.turn == BoardFields.PLAYER1.value:
            color = PLAYER1_COLOR
        elif self.turn == BoardFields.PLAYER2.value:
            color = PLAYER2_COLOR
        else:
            raise Exception("Invalid turn value: ", self.turn)

        self.selected_column = int((mouse_x - BOARD_LEFT_BOUNDARY - GAP / 2) // (2 * POKE_RADIUS + GAP))

        pg.draw.circle(WINDOW, color,
            [
                BOARD_LEFT_BOUNDARY + (POKE_RADIUS + GAP) + self.selected_column * (2 * POKE_RADIUS + GAP),
                HEIGHT_ABOVE_BOARD,
            ],
            POKE_RADIUS)
 
    def start(self):
        while True:
            pg.time.Clock().tick(60)
 
            for event in pg.event.get():
                mouse_x = pg.mouse.get_pos()[0]
 
                match event.type:
                    case pg.QUIT:
                        pg.quit()
                    case pg.MOUSEBUTTONDOWN:
                        if (self.is_mouse_above_board(mouse_x)):
                            self.make_move()
                    case pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            pg.quit()
                        elif event.key == pg.K_r:
                            self.initialize()
 
            self.draw(mouse_x)
            self.check_if_end()

            if self.result != GameResult.NO_RESULT:
                self.end()
 
                while True:
                    event = pg.event.wait()
 
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            pg.quit()
                        elif event.key in [pg.K_RETURN, pg.K_r]:
                            self.initialize()
                            break
 
 
game = Game()
game.start()
