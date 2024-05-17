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

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button, Static
from textual import log, events, on
from textual.binding import Binding
from textual.containers import VerticalScroll
from src.App.widgets.cell import Cell
from src.App.widgets.matrix import Matrix
from src.App.widgets.menu import Menu
from textual.events import Click


class SudokuApp(App):

    CSS_PATH=["./tcss/screen.tcss"]

    TITLE="Sudoku TUI"

    BINDINGS = [Binding("ctrl+z", "suspend_process")]

    def on_mount(self) -> None:
        self.push_screen(Menu())
        #self.screen.styles.background="background-darken-3"
        #self.screen.styles.border= ("round", "background-lighten-3")

    @on (Button.Pressed, "Menu Button")
    def hide_menu(self) -> None:
        self.query_one("Menu", Menu).display=False
    

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