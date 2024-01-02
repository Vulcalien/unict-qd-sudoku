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

# returns a 'size x size' matrix filled with 'val'
def generate_square_matrix(size, val):
    matrix = []
    for i in range(size):
        matrix.append([])
        for j in range(size):
            matrix[i].append(val)
    return matrix

class Sudoku:

    def __init__(self, block_size):
        self.block_size = block_size
        self.size = pow(block_size, 2)

        self.cells = generate_square_matrix(self.size, None)
        self.fixed = generate_square_matrix(self.size, False)

    def get_symbols(self):
        return range(1, self.size + 1)

    # returns True if 'symbol' can be placed in (x, y), False otherwise
    def can_set(self, x, y, symbol):
        # check if the input is valid
        if ((x < 0 or x >= self.size) or
            (y < 0 or y >= self.size) or
            (symbol < 1 or symbol > self.size)):
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

    # try to set 'symbol' in (x, y)
    def set_cell(self, x, y, symbol):
        if not self.can_set(x, y, symbol):
            return False

        self.cells[x][y] = symbol
        return True

    # try to fix 'symbol' in (x, y)
    def set_fixed(self, x, y, symbol):
        if self.set_cell(x, y, symbol):
            self.fixed[x][y] = True
            return True

        return False

    # this can be useful for debugging
    def __str__(self):
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

    # Calculate the coordinates of the next cell.
    # If the right border if reached, the coordinates of the left-most
    # cell of the row beneath are returned.
    # If the given cell is the bottom-right corner of the grid, then the
    # returned coordinates point to a cell outside of the grid.
    def next_cell_coordinates(self, x, y):
        next_x = (x + 1) % self.size
        next_y = y + (x + 1) // self.size
        return (next_x, next_y)

    def has_unique_solution(self):
        return self.has_solutions() == 1

    # recursive backtracking algorithm
    #
    # returns:
    #   '0' if no solution was found
    #   '1' if the solution is unique
    #   more than '1' if there are multiple solutions
    def has_solutions(self, x=0, y=0, count=0):
        # if (x, y) is outside the grid, then a solution was found
        if (x < 0 or x >= self.size) or (y < 0 or y >= self.size):
            return count + 1

        next_x, next_y = self.next_cell_coordinates(x, y)

        # if the cell is fixed, skip it
        if self.fixed[x][y]:
            return self.has_solutions(next_x, next_y, count)

        # try to place every symbol in the cell
        for symbol in self.get_symbols():
            if self.set_cell(x, y, symbol):
                count = self.has_solutions(next_x, next_y, count)

                self.cells[x][y] = None

                # stop searching for solutions after having found more
                # than one
                if count > 1:
                    break

        return count
