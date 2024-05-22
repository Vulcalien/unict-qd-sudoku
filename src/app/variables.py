from widgets.matrix import Matrix, Mode
from typing import Final
SUDOKU_SIZE : Final[int] = 3
sudoku_matrix : Final[Matrix] = Matrix(SUDOKU_SIZE, Mode.STATIC)