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
from textual.widgets import Label, Header, Footer
from textual.app import ComposeResult
from textual.containers import Vertical, Center
from widgets.matrix import Mode, Matrix
from variables import SUDOKU_SIZE
from textual.events import Click


SUDOKU_TEXT : str = """Welcome to Sudoku solve mode!
Use wasd or the arrrow keys to move around.
Use your keyboard to input a number.
When you are ready, press enter and let the magic happen."""


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
    Vertical
    {
        align: center middle;
        content-align: center middle;
    }


"""

    BINDINGS=[
         Binding("q,escape", "main_menu", "Go back to the main menu", show=True),
         Binding("c", "clear", "Clear grid", show=True),
         Binding("enter", "resolve", "Try to resolve the current grid", show=True)
         ]


    def compose(self) -> ComposeResult:
        with Vertical():
            with Center():
                 yield(Label(SUDOKU_TEXT))
            yield Matrix(SUDOKU_SIZE, Mode.STATIC)
        yield Header()
        yield Footer()
            

    def action_main_menu(self) -> None:
            def clean_up(execute: bool) -> None:
                 if(execute):
                    m=self.query_one("Matrix", Matrix)
                    m.set_mode_and_clear(Mode.STATIC)
                    self.app.pop_screen()
                    m.query_cell(0,0).focus()
                    

            self.app.push_screen("quit_screen", clean_up)
    

    def action_clear(self) -> None:
        def clear(execute : bool) -> None:
            if(execute):
                self.query_one("Matrix", Matrix).set_mode_and_clear(Mode.STATIC)
        

        self.app.push_screen("clear_screen", clear)

    def action_resolve(self) -> None:
        self.app.push_screen("error_screen")


    #Seems the only way to make sure clicking on the grid doesn't focus the previous cell
    @on(Click)
    def noOP(self, event : Click):
        event.stop()