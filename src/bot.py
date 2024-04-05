from enums import BoardFields

import numpy as np
import numpy.typing as npt
from random import randint


def get_bot_move(board: npt.NDArray[np.int8], turn: BoardFields) -> int:
    return randint(0, 6)
