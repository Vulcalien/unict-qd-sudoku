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

import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).parent.parent)) #Add directory above so the sudoku module can be imported
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button
from textual import on
from textual.binding import Binding
from widgets.menu import Menu
from widgets.resolve import Resolve
from widgets.play import Play
from widgets.matrix import Matrix, Mode
from widgets.confirm_screen import QuitScreen, ClearScreen
from widgets.error_screen import ErrorScreen
from textual.events import Click



class SudokuApp(App):

    CSS_PATH=["./tcss/screen.tcss"]

    TITLE="Sudoku TUI"

    BINDINGS = [Binding("ctrl+z", "suspend_process")]

    SCREENS = {"menu" : Menu(classes="SudokuScreen"), "play" : Play(classes="SudokuScreen"), "resolve" : Resolve(classes="SudokuScreen"), "quit_screen" : QuitScreen(), "clear_screen" : ClearScreen(), "error_screen" : ErrorScreen()}

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
    



if __name__=="__main__":
    app = SudokuApp()
    app.run() 