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

from textual import on
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Label, Button, Header, Footer
from textual.app import ComposeResult
from textual.containers import VerticalScroll, Center
from widgets.matrix import Matrix, Mode
from constants import MATRIX
from textual.events import Key


SUDOKU_TEXT : str = """Welcome to Sudoku Resolve mode!
Use wasd or the arrrow keys to move around.
Use your keyboard to input a number.
When you are ready, click solve and let the magic happen."""


class Resolve(Screen):
    DEFAULT_CSS="""
    Screen
    {
    align: center middle;
    }
    Button
    {
        height: auto;
        width: 50%;
        margin: 1;
    }
    Matrix
    {
        height: 10fr;
        width: 100%;
        margin: 1;
    }
    Label
    {
        text-align: center;
        align: center middle;
        height: auto;
        margin: 1;
    }
    VerticalScroll
    {
        align: center middle;
        content-align: center middle;
    }


"""

    BINDINGS=[Binding("q,escape", "main_menu", "Go back to the main menu", show=True)]

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            with Center():
                 yield(Label(SUDOKU_TEXT))
            yield(MATRIX)
            with Center():
                 yield(Button("Resolve current sudoku", variant="primary"))
        yield Header()
        yield Footer()
            
    
    async def action_main_menu(self, event : Key):
            self.app.pop_screen()
            self.query_one("Matrix", Matrix).set_mode_and_clear(Mode.STATIC)
