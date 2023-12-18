# Copyright 2023 Vulcalien
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

    # returns True if 'val' can be placed in (x, y), False otherwise
    def can_set(self, x, y, val):
        # check if the input is valid
        if ((x < 0 or x >= self.size) or
            (y < 0 or y >= self.size) or
            (val < 1 or val > self.size)):
               return False

        # check if (x, y) is fixed
        if self.fixed[x][y]:
            return False

        # check the y-th row and x-th column
        for i in range(self.size):
            if val in (self.cells[i][y], self.cells[x][i]):
                return False

        # check the block
        block_x = x // self.block_size
        block_y = y // self.block_size
        for xi in range(block_x, block_x + self.block_size):
            for yi in range(block_y, block_y + self.block_size):
                if self.cells[xi][yi] == val:
                    return False

        return True

    # try to set 'val' in (x, y)
    def set_cell(self, x, y, val):
        if not self.can_set(x, y, val):
            return False

        self.cells[x][y] = val
        return True

    # try to fix 'val' in (x, y)
    def set_fixed(self, x, y, val):
        if not self.can_set(x, y, val):
            return False

        self.fixed[x][y] = True
        self.cells[x][y] = val
        return True

    # clear the fixed status of (x, y)
    def clear_fixed(self, x, y):
        if (x < 0 or x >= self.size) or (y < 0 or y >= self.size):
            return False

        self.fixed[x][y] = False
        return True

    # this can be useful for debugging
    def __str__(self):
        result = ''

        for y in range(self.size):
            for x in range(self.size):
                val = self.cells[x][y]

                if val == None:
                    result += ' _ '
                elif self.fixed[x][y]:
                    result += '[' + str(val) + ']'
                else:
                    result += ' ' + str(val) + ' '
            result += '\n'
        return result
