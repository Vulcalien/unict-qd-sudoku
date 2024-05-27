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

import sys

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header
from textual.binding import Binding
from textual.events import Click

from src.app.widgets.menu import Menu
from src.app.widgets.resolve import Resolve
from src.app.widgets.play import Play
from src.app.widgets.confirm_screen import QuitScreen, ClearScreen, RegenerateScreen
from src.app.widgets.error_screen import ErrorScreen

class SudokuApp(App):

    CSS_PATH=["./tcss/screen.tcss", "./tcss/play.tcss"]

    TITLE="Sudoku TUI"

    BINDINGS = [Binding("ctrl+z", "suspend_process")]

    SCREENS = {
        "menu" : Menu(classes="SudokuScreen"), 
        "play" : Play(classes="SudokuScreen"), 
        "resolve" : Resolve(classes="SudokuScreen"),
        "quit_screen" : QuitScreen(),
        "clear_screen" : ClearScreen(),
        "error_screen" : ErrorScreen(),
        "regenerate_screen" : RegenerateScreen()
        }

    def on_mount(self) -> None:
        self.push_screen(Menu(classes="SudokuScreen"))
        #self.screen.styles.background="background-darken-3"
        #self.screen.styles.border= ("round", "background-lighten-3")
    

    @on(Click)
    def clicked(self):
        cells=self.query("Cell")
        for cell in cells:
            if(cell.has_focus):
                cell.blur()
    


    def compose(self) -> ComposeResult:
        yield Footer()
        yield Header()
        #yield Cell("9", id="testcell")
        #yield Matrix(3, id="matrix")

def main():
    """main function called by a wrapper"""
    app = SudokuApp()
    app.run()
