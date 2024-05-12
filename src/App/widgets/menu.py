from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Button, Static


class Menu(Static):

    DEFAULT_CSS="""
    #menu Button
    {
        margin:1;
        width: 50%;
        height: auto;
    }
    #menu 
    {
    align: center middle;
    }
    """


    def compose(self) -> ComposeResult:
            yield VerticalScroll(
            Button("Play", id="playb", variant="primary"),
            Button("Resolve", id="resolveb", variant="default"),
            id="menu"
        )