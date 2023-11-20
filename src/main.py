import random

from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.containers import Horizontal, Vertical, Container

STYLE_DIR = '../style'

GRID_SIZE = 9

class SudokuApp(App):
    CSS_PATH = STYLE_DIR + '/main.tcss'

    def on_mount(self) -> None:
        pass

    def compose(self) -> ComposeResult:
        with Horizontal(id='app-body'):
            with Vertical(id='left-pane'):
                yield Static('left pane')

            with Container(id='sudoku-grid'):
                for block in range(GRID_SIZE):
                    with Container(classes='sudoku-3x3-block'):
                        for cell in range(GRID_SIZE):
                            test_number = random.randint(1, GRID_SIZE)
                            yield Static(str(test_number),
                                         classes='sudoku-cell')

            with Vertical(id='right-pane'):
                yield Static('right pane')

if __name__ == '__main__':
    app = SudokuApp()
    app.run()
