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
from pytest_mock import MockerFixture

from sudoku import generate_square_matrix
from sudoku import Sudoku

import copy
import random

@pytest.mark.parametrize("size, val", [
    (3, None),
    (7, False),
    (55, 0),
    (0, 'a'),
    (2, 'f')
])
def test_generate_square_matrix(size: int, val: any):
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
def test_sudoku_init(block_size: int, expected_size: int):
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
def test_get_symbols(block_size: int):
    grid = Sudoku(block_size)

    assert grid.get_symbols() == range(1, block_size * block_size + 1)

@pytest.mark.parametrize("block_size, x, y, val", [
    (3, 5, 5, 2),
    (3, 2, 5, 1),
    (3, 1, 5, 1),
    (3, 2, 8, 9),
    (3, 2, 5, 1),
    (2, 2, 2, 2),
    (2, 0, 0, 6),
    (3, -5, 4, None),
    (3, -5, -4, None),
    (3, 4, 9, None),
])
def test_get_cell(block_size: int, x: int, y: int, val: int):
    grid = Sudoku(block_size)

    if x >= 0 and x < block_size**2 and y >= 0 and y < block_size**2:
        grid.cells[x][y] = val

    assert grid.get_cell(x, y) == val

@pytest.mark.parametrize("block_size, x, y, val", [
    (3, 5, 5, False),
    (3, 2, 5, True),
    (3, 1, 5, False),
    (3, 2, 8, True),
    (3, 2, 5, False),
    (2, 2, 2, True),
    (2, 0, 0, False),
    (3, 8, 8, True),
    (3, -1, 0, False),
    (3, -1, -1, False),
    (3, 0, 9, False),
])
def test_is_fixed(block_size: int, x: int, y: int, val: bool):
    grid = Sudoku(block_size)

    if x >= 0 and x < block_size**2 and y >= 0 and y < block_size**2:
        grid.fixed[x][y] = val

    assert grid.is_fixed(x, y) == val

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
def test_can_set_1(block_size: int, to_place: tuple[int, int, int], expected: bool):
    grid = Sudoku(block_size)
    x, y, symbol = to_place

    assert grid._Sudoku__can_set(x, y, symbol) == expected

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
def test_can_set_2(block_size: int, fix: tuple[int, int, int],
                   to_place: [int, int, int], expected: bool):
    grid = Sudoku(block_size)
    fix_x, fix_y, fix_symbol = fix
    x, y, symbol = to_place

    assert grid._Sudoku__set_fixed(fix_x, fix_y, fix_symbol) == True
    assert grid._Sudoku__can_set(x, y, symbol) == expected

@pytest.mark.parametrize("block_size, x, y, next_x, next_y, is_inside", [
    (3, 0, 0, 1, 0, True),
    (3, 8, 0, 0, 1, True),
    (3, 8, 8, 0, 9, False),
    (2, 3, 1, 0, 2, True),
    (4, 4, 4, 5, 4, True),
])
def test_get_next_cell_coordinates(block_size: int, x: int, y: int,
                                   next_x: int, next_y: int, is_inside: bool):
    grid = Sudoku(block_size)

    returned_x, returned_y = grid._Sudoku__get_next_cell_coordinates(x, y)

    assert (returned_x, returned_y) == (next_x, next_y)
    assert grid.is_cell_inside(returned_x, returned_y) == is_inside

@pytest.mark.parametrize("block_size, cell, fixed, expected_str", [
    (3, (0, 0, 5), (1, 1, 3),
        " 5  _  _  _  _  _  _  _  _ \n" +
        " _ [3] _  _  _  _  _  _  _ \n" +
        " _  _  _  _  _  _  _  _  _ \n" +
        " _  _  _  _  _  _  _  _  _ \n" +
        " _  _  _  _  _  _  _  _  _ \n" +
        " _  _  _  _  _  _  _  _  _ \n" +
        " _  _  _  _  _  _  _  _  _ \n" +
        " _  _  _  _  _  _  _  _  _ \n" +
        " _  _  _  _  _  _  _  _  _ \n"),
    (3, (6, 2, 9), (2, 8, 2),
        " _  _  _  _  _  _  _  _  _ \n" +
        " _  _  _  _  _  _  _  _  _ \n" +
        " _  _  _  _  _  _  9  _  _ \n" +
        " _  _  _  _  _  _  _  _  _ \n" +
        " _  _  _  _  _  _  _  _  _ \n" +
        " _  _  _  _  _  _  _  _  _ \n" +
        " _  _  _  _  _  _  _  _  _ \n" +
        " _  _  _  _  _  _  _  _  _ \n" +
        " _  _ [2] _  _  _  _  _  _ \n"),
    (2, (3, 3, 3), (2, 3, 2),
        " _  _  _  _ \n" +
        " _  _  _  _ \n" +
        " _  _  _  _ \n" +
        " _  _ [2] 3 \n")
])
def test_repr(block_size: int, cell: tuple[int, int, int],
              fixed: tuple[int, int, int], expected_str: str):
    grid = Sudoku(block_size)

    grid._Sudoku__set_cell(cell[0], cell[1], cell[2])
    grid._Sudoku__set_fixed(fixed[0], fixed[1], fixed[2])

    assert str(grid) == expected_str

@pytest.mark.parametrize("block_size, cells, expected", [
    (3, [
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
    ], False),
    (2, [
        [None, 2,    None, 4   ],
        [3,    4,    1,    None],
        [None, None, 2,    None],
        [None, None, None, 3   ],
    ], True),
])
def test_has_unique_solution(block_size: int, cells: list[list[int]],
                             expected: bool):
    grid = Sudoku(block_size)

    for y in range(block_size**2):
        for x in range(block_size**2):
            grid._Sudoku__set_fixed(x, y, cells[x][y])

    assert grid.has_unique_solution() == expected

@pytest.mark.parametrize("block_size, cells, expected", [
    (2, [
        [None, 2,    None, 4   ],
        [3,    4,    1,    None],
        [None, None, 2,    None],
        [None, None, None, 3   ],
    ], [
        [1, 2, 3, 4],
        [3, 4, 1, 2],
        [4, 3, 2, 1],
        [2, 1, 4, 3],
    ]),
])
def test_solve_grid(block_size: int, cells: list[list[int]],
                    expected: list[list[int]]):
    grid = Sudoku(block_size)

    for y in range(block_size**2):
        for x in range(block_size**2):
            grid._Sudoku__set_fixed(x, y, cells[x][y])

    grid._Sudoku__solve_grid()

    for y in range(block_size**2):
        for x in range(block_size**2):
            assert grid.cells[x][y] == expected[x][y]

@pytest.mark.parametrize("block_size, cells, expected, expected_unique", [
    (2, [
        [1, 2, 3, 4],
        [3, 4, 1, 2],
        [2, 1, 4, 3],
        [4, 3, 2, 1],
    ], [
        [None, 2, 3, 4],
        [3,    4, 1, 2],
        [2,    1, 4, 3],
        [4,    3, 2, 1],
    ], True),
    (2, [
        [None, None, 2,    None],
        [None, 4,    1,    None],
        [3,    1,    None, None],
        [4,    2,    None, None],
    ], [
        [None, None, 2,    None],
        [None, 4,    1,    None],
        [None, 1,    None, None],
        [4,    2,    None, None],
    ], True),
    (2, [
        [None, None, 2,    None],
        [None, 4,    1,    None],
        [None, 1,    None, None],
        [4,    2,    None, None],
    ], [
        [None, None, 2,    None],
        [None, 4,    1,    None],
        [None, 1,    None, None],
        [None, 2,    None, None],
    ], False),
    (2, [
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
    ], [
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
    ], False)
])
def test_try_to_clear_random_cell(mocker: MockerFixture, block_size: int,
                                  cells:    list[list[tuple[int, bool]]],
                                  expected: list[list[tuple[int, bool]]],
                                  expected_unique: bool):
    grid = Sudoku(block_size)

    for y in range(block_size**2):
        for x in range(block_size**2):
            grid.cells[x][y] = cells[x][y]
            grid.fixed[x][y] = (cells[x][y] is not None)

    mocker.patch.object(
        random, 'sample',
        return_value=range(block_size**2)
    )

    assert grid._Sudoku__try_to_clear_random_cell() == expected_unique

    if expected_unique:
        for y in range(block_size**2):
            for x in range(block_size**2):
                assert grid.cells[x][y] == expected[x][y]
                assert grid.fixed[x][y] == (grid.cells[x][y] is not None)

@pytest.mark.parametrize("block_size, iterations", [
    (3, 10),
    (2, 60),
    (3, 70),
    (3, 100)
])
def test_generate_grid(mocker: MockerFixture, block_size: int,
                       iterations: int):
    grid = Sudoku(block_size)

    mocker.patch.object(
        grid, '_Sudoku__try_to_clear_random_cell',
        return_value=True
    )
    mocker.patch.object(grid, '_Sudoku__fill_grid')
    mocker.patch.object(grid, '_Sudoku__solve_grid')

    spy = mocker.spy(grid, '_Sudoku__try_to_clear_random_cell')

    assert grid.generate_grid(iterations) == iterations

    assert spy.call_count == iterations
