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
from textual.screen import Screen
from textual.app import ComposeResult
from textual.events import Click
from textual.binding import Binding
from textual.containers import Grid, Center, Middle
from textual.widgets import Header, Footer, Static
from textual.reactive import Reactive

from src.sudoku import Sudoku
from src.app.widgets.matrix import Matrix, Mode
from src.app.variables import SUDOKU_SIZE

class Play(Screen):

    
    remaining_cells : Reactive[int]=Reactive(0)
    errors : Reactive[int]=Reactive(0)



    BINDINGS=[Binding("q,escape", "main_menu", "Go back to main menu", show=True),
              Binding("r", "regenerate", "Regenerate puzzle", show=True)]

    def compose(self) -> ComposeResult:
        with Grid():
            yield Static("", id="status", classes="PlayText")
            yield Static("Welcome to sudoku! Move the cells with wasd or the arrow keys. Input a digit with your keyboard. Have Fun!",id="how_to", classes="PlayText")
            yield Static(id="timer", classes="PlayText")
        with Center():
            yield Matrix(SUDOKU_SIZE, Mode.ACTIVE, id="play_matrix")
        yield Header()
        yield Footer()


    def gen_and_load(self) -> None:
        sudoku : Sudoku = Sudoku(SUDOKU_SIZE)
        sudoku.generate_grid(65)
        m : Matrix = self.query_one("Matrix", Matrix)
        m.clear_and_load(Mode.ACTIVE, sudoku)
        self.errors=0
        self.remaining_cells=SUDOKU_SIZE**4-m.number_of_hints()
        

    def on_mount(self) -> None:
        self.gen_and_load()


    def action_main_menu(self) -> None:
        def clean_up(execute: bool) -> None:
                if(execute):
                    m=self.query_one("Matrix", Matrix)
                    self.gen_and_load()
                    self.app.pop_screen()
                    m.query_cell(0,0).focus()
                    
        self.app.push_screen("quit_screen", clean_up)

    
    def action_regenerate(self) -> None:
            def regen(execute: bool) -> None:
                if(execute):
                    self.gen_and_load()


            self.app.push_screen("regenerate_screen", regen)


    def watch_errors(self) -> None:
        self.update_status()


    def watch_remaining_cells(self) -> None:
        self.update_status()
        if(self.remaining_cells==0):
            pass #TODO: Make something happen when the user completes the puzzle

    def update_status(self) -> None:
        text =  "[bold green]Remaining Cells: [/bold green]" + \
               f"[bold]{self.remaining_cells}[/bold]" + "\n" + \
                "[bold red]Errors: [/bold red]"              + \
               f"[bold]{self.errors}[/bold]"
        self.query_one("#status", Static).update(text)


    @on(Matrix.Modified)
    def modified_matrix(self, modified : Matrix.Modified) -> None:
        cell=modified.cell
        if cell.has_class("error"):
            self.errors+=1
        elif cell.has_class("correct"):
            self.remaining_cells-=1
    

    #Seems the only way to make sure clicking on the grid doesn't focus the previous cell
    @on(Click)
    def noOP(self, event : Click):
        event.stop()
