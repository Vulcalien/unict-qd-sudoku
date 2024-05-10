# Copyright 2023-2024 Vulcalien
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

import random

def generate_square_matrix(size: int, val: any) -> list[list[int]]:
    """returns a 'size x size' matrix filled with 'val'"""
    matrix = []
    for i in range(size):
        matrix.append([])
        for j in range(size):
            matrix[i].append(val)
    return matrix

class Sudoku:

    def __init__(self, block_size: int):
        self.block_size = block_size
        self.size = pow(block_size, 2)

        self.cells = generate_square_matrix(self.size, None)
        self.fixed = generate_square_matrix(self.size, False)

    def get_symbols(self) -> list[int]:
        """returns an ordered list of all the allowed symbols"""
        return range(1, self.size + 1)

    def is_cell_inside(self, x: int, y: int) -> bool:
        """returns True if (x, y) is inside the grid, False otherwise"""
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            return False
        return True

    def can_set(self, x: int, y: int, symbol: int) -> bool:
        """returns True if 'symbol' can be placed in (x, y), False otherwise"""
        # check if the input is valid
        if (not self.is_cell_inside(x, y) or
            symbol not in self.get_symbols()):
            return False

        # check if (x, y) is fixed
        if self.fixed[x][y]:
            return False

        # check the y-th row and x-th column
        for i in range(self.size):
            if symbol in (self.cells[i][y], self.cells[x][i]):
                return False

        # check the block
        block_x0 = (x // self.block_size) * self.block_size
        block_y0 = (y // self.block_size) * self.block_size
        for xi in range(block_x0, block_x0 + self.block_size):
            for yi in range(block_y0, block_y0 + self.block_size):
                if self.cells[xi][yi] == symbol:
                    return False

        return True

    def set_cell(self, x: int, y: int, symbol: int) -> bool:
        """try to set 'symbol' in (x, y)"""
        if not self.can_set(x, y, symbol):
            return False

        self.cells[x][y] = symbol
        return True

    def set_fixed(self, x: int, y: int, symbol: int) -> bool:
        """try to fix 'symbol' in (x, y)"""
        if self.set_cell(x, y, symbol):
            self.fixed[x][y] = True
            return True
        return False

    def clear_fixed(self, x: int, y: int) -> bool:
        """clear the fixed status of (x, y)"""
        if not self.is_cell_inside(x, y):
            return False

        self.fixed[x][y] = False
        return True

    def get_next_cell_coordinates(self, x: int, y: int) -> tuple[int, int]:
        """Returns the coordinates of the next cell.
        It acts as if cells were ordered top-to-bottom then
        left-to-right. So, if (x, y) is a cell in the right border, the
        returned value will be (0, y+1).
        If (x, y) is the bottom-right corner of the grid, the returned
        coordinates point to a non-existent cell outside of the grid.
        """
        next_x = (x + 1) % self.size
        next_y = y + (x + 1) // self.size
        return (next_x, next_y)

    def has_unique_solution(self) -> bool:
        """returns True if the grid has one unique solution, False otherwise"""
        return self.__has_solutions() == 1

    def __has_solutions(self, x=0, y=0, count=0) -> int:
        """Recursive backtracking algorithm.
        Returns:
            '0' if no solution was found
            '1' if the solution is unique
            more than '1' if there are multiple solutions
        """

        # if (x, y) is outside the grid, then a solution was found
        if not self.is_cell_inside(x, y):
            return count + 1

        next_x, next_y = self.get_next_cell_coordinates(x, y)

        # if the cell is fixed, skip it
        if self.fixed[x][y]:
            return self.__has_solutions(next_x, next_y, count)

        old_symbol = self.cells[x][y]

        # try to place every symbol in the cell
        for symbol in self.get_symbols():
            if self.set_cell(x, y, symbol):
                count = self.__has_solutions(next_x, next_y, count)
                self.cells[x][y] = old_symbol

                # multiple solutions were found: stop searching for more
                if count > 1:
                    break
        return count

    def generate_grid(self, iterations: int) -> int:
        self.__fill_grid(0, 0)

        count = 0
        for i in range(iterations):
            print('iteration: ', i)
            if self.__try_to_clear_random_cell():
                count += 1
        return count

    def __fill_grid(self, x: int, y: int) -> bool:
        """randomly fill a grid with fixed values"""

        # if (x, y) is outside the grid, then the grid is entirely full
        if not self.is_cell_inside(x, y):
            return True

        next_x, next_y = self.get_next_cell_coordinates(x, y)
        symbols = random.sample(self.get_symbols(), k=self.size)

        # try to place every symbol in the cell
        for symbol in symbols:
            if self.set_fixed(x, y, symbol):
                if self.__fill_grid(next_x, next_y):
                    return True # the grid is full

                # this symbol didn't work: go back
                self.cells[x][y] = None
                self.fixed[x][y] = False

        # no symbol could be placed
        return False

    def __try_to_clear_random_cell(self) -> bool:
        """attempt to remove one symbol from the grid while maintaining
        uniqueness of the solution"""

        # find (x, y) coordinates of a random fixed cell
        for y in random.sample(range(self.size), k=self.size):
            for x in random.sample(range(self.size), k=self.size):
                if self.fixed[x][y]:
                    break

        # clear the cell
        symbol = self.cells[x][y]
        self.cells[x][y] = None
        self.fixed[x][y] = False

        # check if the solution is still unique
        if not self.has_unique_solution():
            # if not, put the symbol back
            self.cells[x][y] = symbol
            self.fixed[x][y] = True
            return False # the cell could not be cleared

        # the cell was successfully cleared
        return True

    def __repr__(self) -> str:
        result = ''

        for y in range(self.size):
            for x in range(self.size):
                symbol = self.cells[x][y]

                if symbol == None:
                    result += ' _ '
                elif self.fixed[x][y]:
                    result += '[' + str(symbol) + ']'
                else:
                    result += ' ' + str(symbol) + ' '
            result += '\n'
        return result
