# Copyright 2024 Henrysk
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

from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Grid
from textual.widgets import Placeholder
from variables import sudoku_matrix

class Play(Screen):
    DEFAULT_CSS="""
    Grid {
        grid-size: 3 2;
    }
    Matrix
    {
        column-span: 3;
    }
    Placeholder
    {
        width: 1fr;
        height: auto;
    }
    """
    def compose(self) -> ComposeResult:
        with Grid():
            yield Placeholder(id="state_text")
            yield Placeholder(id="how_to")
            yield Placeholder(id="timer")
            yield sudoku_matrix
