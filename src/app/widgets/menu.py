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

from textual import on, log
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Button, Footer, Header
from textual.screen import Screen

class Menu(Screen):

    DEFAULT_CSS="""
    VerticalScroll Button {
        margin:1;
        width: 50%;
        height: auto;
        color: $text;
    }

    VerticalScroll {
        align: center middle;
    }

    #resolveb {
        display: none;
    }
    """

    def compose(self) -> ComposeResult:
        yield VerticalScroll(
            Button("Play", id="playb", variant="primary"),
            Button("Solve", id="resolveb", variant="default", disabled=True),
            id="menu"
        )
        yield Footer()
        yield Header()

    @on(Button.Pressed, "#resolveb")
    def resolve(self, event : Button.Pressed) -> None:
        log.debug("Resolve sudoku mode selected!")
        self.app.push_screen("resolve")

    @on(Button.Pressed, "#playb")
    def play(self, event : Button.Pressed) -> None:
        self.app.push_screen("play")
