from enum import Enum


class BoardFields(Enum):
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2


class GameResult(Enum):
    NO_RESULT = -1
    TIE = 0
    PLAYER1_WIN = 1
    PLAYER2_WIN = 2
