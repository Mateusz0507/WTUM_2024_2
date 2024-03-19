import sys
import numpy as np
import numpy.typing as npt
import pygame as pg
from pygame import gfxdraw
from bot import get_bot_move
from enums import BoardFields, GameResult

# Window
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
FPS = 60
TITLE = "Connect Four"

# UI
DISC_RADIUS = min(WINDOW_WIDTH / 20, WINDOW_HEIGHT / 20)
GAP = DISC_RADIUS / 2
BOARD_LEFT_BOUNDARY = WINDOW_WIDTH / 2 - (7 * DISC_RADIUS + 4 * GAP)
BOARD_WIDTH = 14 * DISC_RADIUS + 8 * GAP
BOARD_RIGHT_BOUNDARY = BOARD_LEFT_BOUNDARY + BOARD_WIDTH
BOARD_TOP_BOUNDARY = (
    WINDOW_HEIGHT / 2 - (6 * DISC_RADIUS + 3.5 * GAP) + (2 * DISC_RADIUS + GAP) / 2
)
BOARD_HEIGHT = 12 * DISC_RADIUS + 7 * GAP
BOARD_BOTTOM_BOUNDARY = BOARD_TOP_BOUNDARY + BOARD_HEIGHT
HEIGHT_ABOVE_BOARD = BOARD_TOP_BOUNDARY - (GAP + DISC_RADIUS)

# Colors
BACKGROUND_COLOR = pg.Color("black")
TEXT_COLOR = pg.Color("white")
BOARD_COLOR = pg.Color("blue")
PLAYER1_COLOR = pg.Color("yellow")
PLAYER2_COLOR = pg.Color("red")

# Game
LINE_OF_4 = 4
BOARD_ROWS = 6
BOARD_COLUMNS = 7

# Why pg.init() is necessary: https://stackoverflow.com/a/58868533/13371509
pg.init()
window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption(TITLE)


class Game:
    empty_board: npt.NDArray[np.int8] = np.full(
        (BOARD_COLUMNS, BOARD_ROWS), BoardFields.EMPTY.value, dtype="int8"
    )

    def __init__(self, bot_turn: BoardFields) -> None:
        self.bot_turn: BoardFields = bot_turn
        self.reset()

    def reset(self) -> None:
        self.board = Game.empty_board.copy()
        self.result = GameResult.NO_RESULT
        self.turn = BoardFields.PLAYER1
        self.last_move: tuple[int, int] | None = None
        self.selected_column: int | None = None

    def make_move(self) -> None:
        if self.selected_column is None:
            return

        for row in range(BOARD_ROWS):
            if self.board[self.selected_column, row] == BoardFields.EMPTY.value:
                self.board[self.selected_column, row] = self.turn.value
                self.last_move = (self.selected_column, row)
                self.turn = (
                    BoardFields.PLAYER1
                    if self.turn == BoardFields.PLAYER2
                    else BoardFields.PLAYER2
                )
                return

    def is_mouse_above_board(self, mouse_x: int) -> int:
        return BOARD_LEFT_BOUNDARY + GAP / 2 < mouse_x < BOARD_RIGHT_BOUNDARY - GAP / 2

    def update_result(self) -> None:
        if self.check_if_player_won(BoardFields.PLAYER1):
            self.result = GameResult.PLAYER1_WIN
        elif self.check_if_player_won(BoardFields.PLAYER2):
            self.result = GameResult.PLAYER2_WIN
        elif np.count_nonzero(self.board == BoardFields.EMPTY.value) == 0:
            self.result = GameResult.TIE
        # If none of conditionts above are false,
        # self.result is GameResult.NoResult

    def check_if_player_won(self, player: BoardFields) -> bool:
        if self.last_move is None:
            return False

        column = self.last_move[0]
        first_start_column = max(column - (LINE_OF_4 - 1), 0)
        last_start_column = min(column, (BOARD_COLUMNS - 1) - (LINE_OF_4 - 1))
        starting_columns = list(range(first_start_column, last_start_column + 1))

        row = self.last_move[1]
        first_start_row = max(row - (LINE_OF_4 - 1), 0)
        last_start_row = min(row, (BOARD_ROWS - 1) - (LINE_OF_4 - 1))
        starting_rows = list(range(first_start_row, last_start_row + 1))

        # HORIZONTAL _
        for i in range(len(starting_columns)):
            line_columns = [starting_columns[i] + j for j in range(LINE_OF_4)]
            if (
                np.count_nonzero(self.board[line_columns, row] == player.value)
                == LINE_OF_4
            ):
                return True

        # VERTICAL |
        for i in range(len(starting_rows)):
            line_rows = [starting_rows[i] + j for j in range(LINE_OF_4)]
            if (
                np.count_nonzero(self.board[column, line_rows] == player.value)
                == LINE_OF_4
            ):
                return True

        # DIAGONAL /
        for i in range(min(len(starting_columns), len(starting_rows))):
            line_columns = [starting_columns[i] + j for j in range(LINE_OF_4)]
            line_rows = [starting_rows[i] + j for j in range(LINE_OF_4)]
            if (
                np.count_nonzero(self.board[line_columns, line_rows] == player.value)
                == LINE_OF_4
            ):
                return True

        # DIAGONAL \
        first_start_row = max(row, LINE_OF_4 - 1)
        last_start_row = min(row + (LINE_OF_4 - 1), BOARD_ROWS - 1)
        # Special case - check backwards
        starting_rows = list(range(first_start_row, last_start_row + 1))
        starting_columns = list(range(last_start_column, first_start_column - 1, -1))

        for i in range(min(len(starting_columns), len(starting_rows))):
            line_columns = [starting_columns[i] + j for j in range(LINE_OF_4)]
            line_rows = [starting_rows[i] - j for j in range(LINE_OF_4)]
            if (
                np.count_nonzero(self.board[line_columns, line_rows] == player.value)
                == LINE_OF_4
            ):
                return True

        return False

    def show_endscreen(self):
        window.fill(BACKGROUND_COLOR)
        self.draw_board()

        match self.result:
            case GameResult.PLAYER1_WIN:
                message = "PLAYER 1 WON"
                color = PLAYER1_COLOR
            case GameResult.PLAYER2_WIN:
                message = "PLAYER 2 WON"
                color = PLAYER2_COLOR
            case GameResult.TIE:
                message = "DRAW"
                color = TEXT_COLOR
            case _:
                raise Exception("Invalid result value: ", self.result)

        text = pg.font.Font(None, int(2 * DISC_RADIUS)).render(message, True, color)
        text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, HEIGHT_ABOVE_BOARD))
        window.blit(text, text_rect)

        pg.display.update()

    def draw(self, mouse_x: int) -> None:
        window.fill(BACKGROUND_COLOR)
        self.draw_board()

        if self.is_mouse_above_board(mouse_x):
            self.draw_disc_above_board(mouse_x)

        pg.display.update()

    def draw_board(self) -> None:
        pg.draw.rect(
            window,
            BOARD_COLOR,
            [BOARD_LEFT_BOUNDARY, BOARD_TOP_BOUNDARY, BOARD_WIDTH, BOARD_HEIGHT],
        )

        for column in range(BOARD_COLUMNS):
            for row in range(BOARD_ROWS):
                match self.board[column, row]:
                    case BoardFields.EMPTY.value:
                        color = BACKGROUND_COLOR
                    case BoardFields.PLAYER1.value:
                        color = PLAYER1_COLOR
                    case BoardFields.PLAYER2.value:
                        color = PLAYER2_COLOR
                    case _:
                        raise Exception("Invalid color value: ", BoardFields.EMPTY)

                x = int(
                    BOARD_LEFT_BOUNDARY
                    + (DISC_RADIUS + GAP)
                    + column * (2 * DISC_RADIUS + GAP)
                )
                y = int(
                    BOARD_BOTTOM_BOUNDARY
                    - (DISC_RADIUS + GAP)
                    - row * (2 * DISC_RADIUS + GAP)
                )
                self.draw_disc(x, y, color)

    def draw_disc(self, x: int, y: int, color: pg.Color):
        shadow_color = pg.Color(color[0] // 2, color[1] // 2, color[2] // 2)

        gfxdraw.aacircle(window, int(x), int(y), int(DISC_RADIUS), shadow_color)
        gfxdraw.filled_circle(window, int(x), int(y), int(DISC_RADIUS), shadow_color)

        gfxdraw.aacircle(window, int(x), int(y), int(2 / 3 * DISC_RADIUS), color)
        gfxdraw.filled_circle(window, int(x), int(y), int(2 / 3 * DISC_RADIUS), color)

    def draw_disc_above_board(self, mouse_x):
        match self.turn:
            case BoardFields.PLAYER1:
                color = PLAYER1_COLOR
            case BoardFields.PLAYER2:
                color = PLAYER2_COLOR
            case _:
                raise Exception("Invalid turn value: ", self.turn)

        self.selected_column = int(
            (mouse_x - BOARD_LEFT_BOUNDARY - GAP / 2) // (2 * DISC_RADIUS + GAP)
        )

        x = int(
            BOARD_LEFT_BOUNDARY
            + (DISC_RADIUS + GAP)
            + self.selected_column * (2 * DISC_RADIUS + GAP)
        )
        y = int(HEIGHT_ABOVE_BOARD)
        self.draw_disc(x, y, color)

    def start(self) -> None:
        clock = pg.time.Clock()

        while True:
            clock.tick(FPS)

            for event in pg.event.get():
                mouse_x = pg.mouse.get_pos()[0]

                match event.type:
                    case pg.QUIT:
                        self.gracefully_exit()
                    case pg.MOUSEBUTTONDOWN:
                        if self.is_mouse_above_board(mouse_x):
                            self.make_move()
                    case pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            self.gracefully_exit()
                        elif event.key == pg.K_r:
                            self.reset()

            self.draw(mouse_x)
            self.update_result()

            if self.bot_turn == self.turn:
                self.selected_column = get_bot_move(self.board, self.turn)
                self.make_move()

            if self.result != GameResult.NO_RESULT:
                self.show_endscreen()

                while True:
                    event = pg.event.wait()

                    if event.type == pg.QUIT:
                        pg.quit()
                    elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            pg.quit()
                        elif event.key in [pg.K_RETURN, pg.K_r]:
                            self.reset()
                            break

    def gracefully_exit(self) -> None:
        pg.display.quit()
        pg.quit()
        sys.exit(0)


if __name__ == "__main__":
    game = Game(BoardFields.PLAYER2)
    game.start()
