from typing import Final

from src.app.widgets.matrix import Matrix, Mode

SUDOKU_SIZE : Final[int] = 3
sudoku_matrix : Final[Matrix] = Matrix(SUDOKU_SIZE, Mode.STATIC)
