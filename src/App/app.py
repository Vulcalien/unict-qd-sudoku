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

    CSS_PATH="./tcss/screen.tcss"

    TITLE="Sudoku TUI"

    BINDINGS = [Binding("ctrl+z", "suspend_process")]

    def on_mount(self) -> None:
        pass
        #self.screen.styles.background="background-darken-3"
        #self.screen.styles.border= ("round", "background-lighten-3")

    @on (Button.Pressed, "Menu Button")
    def hide_menu(self) -> None:
        self.query_one("Menu", Menu).display=False
    
    @on (Button.Pressed, "#resolveb")
    def resolve(self) -> None:
        log.debug("Resolve sudoku mode selected!")

    @on (Button.Pressed, "#playb")
    def play(self) -> None:
        log.debug("Play sudoku mode selected!")

    @on(Click)
    def clicked(self):
        cells=self.query("Cell")
        for cell in cells:
            if(cell.has_focus):
                cell.blur()
    


    def compose(self) -> ComposeResult:
        yield Footer()
        #yield Menu()
        yield Header()
        #yield Cell("9", id="testcell")
        yield Matrix(3, id="matrix")
    

if __name__=="__main__":
    app = SudokuApp()
    app.run() 