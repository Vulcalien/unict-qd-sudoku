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
from textual.events import Click, Key
from textual.message import Message
from textual.reactive import Reactive
from textual.widgets import Static

from rich.console import ConsoleRenderable, RichCast

class Cell(Static):

    class Modified(Message):
         def __init__(self, css_class : str, old_digit : str) -> None:
              self.css_class=css_class
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
          background: $success;
    }
    &.correct.hint
    {
          background: $primary;
    }
    &.error
    {
          border: tall $error;
          background: $error;
    }
    &:dark
    {
        border: tall white;
    }
    &:hover
    {
        border: tall $accent;
    }
    &:focus
    {
        border: tall $secondary;
    }
    border: tall black;
    width: 7;
    height: 3;
    content-align: center middle;
    margin: 0;
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
         #Ignore input if the guess is (already) correct
         if(key.character is not None and "correct" not in self.classes and ((key.character>="1" and key.character<="9") or key.key=="backspace")):
               self.old_digit=self.digit
               self.digit=key.character
               if(self.classes is not None):
                    for s in self.classes:
                         if ("cell" in s):
                              self.post_message(self.Modified(s, self.old_digit))
                              break

    def watch_digit(self) -> None:
         self.update(self.digit)
