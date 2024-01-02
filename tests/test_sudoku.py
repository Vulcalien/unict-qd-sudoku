# Copyright 2024 Vulcalien
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pytest

from sudoku import generate_square_matrix
from sudoku import Sudoku

@pytest.mark.parametrize("size, val", [
    (3, None),
    (7, False),
    (55, 0),
    (0, 'a'),
    (2, 'f')
])
def test_generate_square_matrix(size, val):
    matrix = generate_square_matrix(size, val)

    # check that the size is correct
    assert size == len(matrix)
    for row in matrix:
        assert size == len(row)

    # check that 'val' was actually placed in the matrix
    for row in matrix:
        for element in row:
            assert element == val


@pytest.mark.parametrize("block_size, expected_size", [
    (0, 0),
    (1, 1),
    (2, 4),
    (3, 9),
    (9, 81)
])
def test_sudoku_init(block_size, expected_size):
    grid = Sudoku(block_size)

    assert grid.block_size == block_size
    assert grid.size == expected_size

    # check that no cell has a value or is fixed
    for y in range(grid.size):
        for x in range(grid.size):
            assert grid.cells[x][y] == None
            assert grid.fixed[x][y] == False

@pytest.mark.parametrize("block_size", [
    1, 2, 3, 4, 9
])
def test_get_symbols(block_size):
    grid = Sudoku(block_size)

    assert grid.get_symbols() == range(1, block_size * block_size + 1)

@pytest.mark.parametrize("block_size, to_place, expected", [
    (1, (0, 0, -1), False),
    (1, (0, 0, 0), False),
    (1, (0, 0, 1), True),
    (2, (0, 0, 1), True),
    (2, (0, 0, 2), True),
    (2, (0, 0, 3), True),
    (2, (0, 0, 4), True),
    (2, (0, 0, 5), False),
    (3, (-1, 0, 1), False),
    (3, (0, -1, 2), False),
    (4, (-5, -5, 2), False),
    (9, (80, 80, 1), True),
    (9, (80, 80, 80), True),
    (3, (8, 8, 0), False),
    (3, (8, 8, 9), True),
    (3, (5, 3, 5), True),
    (3, (8, 4, 3), True)
])
def test_can_set_1(block_size, to_place, expected):
    grid = Sudoku(block_size)
    x, y, symbol = to_place

    assert grid.can_set(x, y, symbol) == expected

@pytest.mark.parametrize("block_size, fix, to_place, expected", [
    (1, (0, 0, 1), (0, 0, 1), False),
    (3, (2, 2, 3), (2, 2, 3), False),
    (3, (2, 2, 3), (1, 1, 8), True),
    (3, (2, 2, 3), (1, 1, 3), False),
    (3, (2, 2, 5), (0, 2, 5), False),
    (3, (2, 2, 5), (0, 2, 3), True),
    (3, (0, 0, 9), (8, 0, 9), False),
    (3, (0, 0, 9), (8, 0, 7), True),
    (3, (8, 8, 1), (7, 7, 1), False),
    (3, (8, 8, 1), (6, 7, 1), False),
    (3, (8, 8, 1), (7, 6, 1), False),
    (3, (8, 8, 1), (6, 6, 1), False),
    (3, (8, 8, 1), (7, 5, 1), True),
    (3, (8, 8, 1), (7, 5, 99), False),
    (3, (8, 8, 1), (7, 5, -1), False),
    (3, (8, 8, 1), (-1, 5, 1), False),
    (3, (8, 8, 1), (-1, 5, 1), False),
    (3, (8, 8, 1), (-1, -1000, 1), False),
    (3, (3, 3, 1), (3, 3, 2), False),
    (3, (3, 3, 1), (3, 4, 2), True),
    (3, (3, 3, 1), (4, 3, 2), True),
    (3, (3, 3, 9), (3, 4, 9), False),
    (3, (3, 3, 9), (3, 4, 4), True),
    (3, (3, 3, 9), (3, 3, 10), False),
])
def test_can_set_2(block_size, fix, to_place, expected):
    grid = Sudoku(block_size)
    fix_x, fix_y, fix_symbol = fix
    x, y, symbol = to_place

    assert grid.set_fixed(fix_x, fix_y, fix_symbol) == True
    assert grid.can_set(x, y, symbol) == expected
