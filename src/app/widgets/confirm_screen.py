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

from textual.screen import ModalScreen
from textual.widgets import Button, Label
from textual.app import ComposeResult
from textual.containers import Grid

class ConfirmScreen(ModalScreen[bool]):  
    """Screen with a dialog to confirm an action."""

    DEFAULT_CSS="""
    .ConfirmScreen {
        align: center middle;
    }

    .Dialog {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: 1fr 3;
        padding: 0 1;
        width: 50%;
        height: 50%;
        border: tall $warning 80%;
        background: $surface;
    }

    .Question {
        column-span: 2;
        height: 1fr;
        width: 1fr;
        content-align: center middle;
    }

    .ConfirmScreen Button {
        width: 100%;
    }
"""

    def __init__(self, question : str, positive_answer : str, negative_answer : str,  name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        self.question=question
        self.positive_answer=positive_answer
        self.negative_answer=negative_answer
        super().__init__(name, id, classes)



    def compose(self) -> ComposeResult:
                yield Grid(
            Label(self.question, classes="Question"),
            Button(self.positive_answer, variant="error", classes="PosAns"),
            Button(self.negative_answer, variant="primary", classes="NegAnsw"),
            classes="Dialog",
        )

    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.has_class("PosAns"):
            self.dismiss(True)
        else:
            self.dismiss(False)


class QuitScreen(ConfirmScreen):
    def __init__(self, name: str | None = None, id: str | None = None) -> None:
        super().__init__("Are you sure you want to quit? Progress will be lost!","Quit","Cancel", name, id, "ConfirmScreen")


class ClearScreen(ConfirmScreen):
     def __init__(self, name: str | None = None, id: str | None = None) -> None:
          super().__init__("Are you sure you want to clear the grid? Progress will be lost!", "Yes", "No", name, id, "ConfirmScreen")

class RegenerateScreen(ConfirmScreen):
    def __init__(self, name: str | None = None, id: str | None = None) -> None:
        super().__init__("Are you sure you want to regenerate the puzzle? Progress will be lost!","Yes","No", name, id, "ConfirmScreen")
