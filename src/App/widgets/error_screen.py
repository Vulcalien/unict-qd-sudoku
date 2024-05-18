from textual.screen import ModalScreen
from textual.widgets import Button, Label
from textual.containers import VerticalScroll, Center
from textual.app import ComposeResult
from textual import on

ERROR_MESSAGE="""The sudoku grid you inserted does not have an unique solution."""

class ErrorScreen(ModalScreen):
    """Screen that shows an error when trying to resolve the sudoku"""
    DEFAULT_CSS="""
    ErrorScreen
    {
        align: center middle;
    }
    Label
    {
        text-align: center;
        content-align: center top;
        margin: 1;
        width: 1fr;
    }
    VerticalScroll
    {
        border: tall $error;
        content-align: center middle;
        width: 50%;
        height: auto;
    }
    Button
    {
        margin: 1;
        align: center bottom;
        width: 1fr
    }
"""
    def compose(self) -> ComposeResult:
            with VerticalScroll():
                yield Label(ERROR_MESSAGE)
                yield Button("Ok", variant="error")
    
    
    @on(Button.Pressed)
    def go_back(self):
        self.app.pop_screen()
    
