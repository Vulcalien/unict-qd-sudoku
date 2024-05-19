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
from textual.binding import Binding
from textual.containers import Grid, Center, HorizontalScroll
from textual.widgets import Placeholder, Header, Footer
from variables import SUDOKU_SIZE
from sudoku import Sudoku
from widgets.matrix import Matrix, Mode

class Play(Screen):
    DEFAULT_CSS="""
    Matrix
    {
        width: 1fr;
        height: 1fr;
        align: center middle;
    }
    Placeholder
    {
        width: 1fr;
        height: 1;
    }
    """

    BINDINGS=[Binding("q,escape", "main_menu", "Go back to main menu", show=True)]

    def compose(self) -> ComposeResult:
        with HorizontalScroll():
            yield Placeholder(id="state_text")
            yield Placeholder(id="how_to")
            yield Placeholder(id="timer")
        with Center():
            yield Matrix(SUDOKU_SIZE, Mode.ACTIVE)
        yield Header()
        yield Footer()


    def on_mount(self):
        sudoku=Sudoku(SUDOKU_SIZE)
        sudoku.generate_grid(65)
        self.query_one("Matrix", Matrix).clear_and_load(Mode.ACTIVE, sudoku)


    def action_main_menu(self) -> None:
        self.app.pop_screen()
        self.on_mount()
