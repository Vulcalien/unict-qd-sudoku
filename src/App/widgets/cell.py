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

from rich.console import ConsoleRenderable, RichCast
from textual import on
from textual.events import Click, Key
from textual.message import Message
from textual.reactive import Reactive
from textual.widgets import Static

class Cell(Static):

    class Modified(Message):
         def __init__(self, id : str, old_digit : str) -> None:
              self.id=id
              self.old_digit=str  
              super().__init__()       

    #A digit or a space string
    digit : Reactive[str] = Reactive(" ")

    def __init__(self, digit : str, renderable: ConsoleRenderable | RichCast | str = "", *, expand: bool = False, shrink: bool = False, markup: bool = True, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
         super().__init__(renderable, expand=expand, shrink=shrink, markup=markup, name=name, id=id, classes=classes, disabled=disabled)
         self.digit=digit


    #Technically I could do a more generalized version of this (NxN sudokus), for now I'll stick to classic cells found in 3x3 sudokus
    def validate_digit(self, character : str) -> str:
         if(character>"9" or character <"1"):
              return " "
         return character

    DEFAULT_CSS="""
    Cell {
    background: $background-darken-3;
    color: $text;
    &.correct
    {
          border: tall $success;
          color: $success;
    }
    &.error
    {
          border: tall $error;
          color: $error;
    }
    &:dark
    {
        border: tall white;
    }
    &:hover
    {
        border: tall $accent;
        color: $accent;
    }
    &:focus
    {
        border: tall $secondary;
        color: $secondary;
    }
    border: tall black;
    width: auto;
    height: auto;
    content-align: center middle;
    padding: 0 2;
    }"""

    def on_mount(self) -> None:
        self.update(str(self.digit))
        self.can_focus=True


    @on(Click)
    def clicked(self, event: Click) -> None:
         self.focus()
         event.stop()


    @on(Key)
    def key_press(self, key : Key) -> None:
         if(key.character is not None):
            if(self.validate_digit(key.character)!=' ' or key.key=="backspace"):
                self.old_digit=self.digit
                self.digit=key.character
                self.post_message(self.Modified(self.id, self.old_digit))

    def watch_digit(self) -> None:
         self.update(self.digit)