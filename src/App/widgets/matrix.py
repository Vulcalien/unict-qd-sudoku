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

from src.App.widgets.cell import Cell

from textual import log
from textual import on
from textual.events import DescendantBlur, Blur
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Grid
from textual.widget import Widget
from typing import Iterable, List

class Matrix(Grid):

     DEFAULT_CSS="""
     Matrix
     {
        padding: 0;
        margin: 0;
        overflow: auto auto;
        grid-gutter: 0;
     }
"""
     BINDINGS=[
          Binding("w,up", "go_up", "Go one cell above", show=False),
          Binding("s,down", "go_down", "Go one cell below", show=False),
          Binding("d,right", "go_right", "Go on cell to the right", show=False),
          Binding("a,left", "go_left", "Go one cell to the left", show=False)
          #Binding("c", "clear", "Clears the cells", show=False)
          ]
     

     
     def to_iterable(self) -> Iterable[Iterable[str]]:
          for y in range(self.line_size):
                    yield (cell.digit for cell in (self.query_one(f"#cell_{x}_{y}", Cell) for x in range(self.line_size)))

     def to_list(self) -> List[List[str]]:
           return [list(x) for x in self.to_iterable()]


     def move_to(self, x: int, y:int) -> None:
          self.query_one(f"#cell_{x}_{y}",Cell).focus()


     def extract_position(self, cell : Cell) -> tuple[int, int]:
          """Extracts x and y coordinates from a cell"""
          return tuple(int(i) for i in ((cell.id.split("_"))[1:]))
     

     def get_currently_focused_position(self) -> tuple[int,int]:
          return self.extract_position(self.query_one("Cell:focus",Cell))
     
     def get_currently_focused(self) -> Cell:
          return self.query_one("Cell:focus", Cell)

     @on(Cell.Modified)
     def modified(self, modified : Cell.Modified) -> None:
          log.debug(self.to_list())
          modif_cell=self.query_one("#"+modified.id, Cell)
          #TODO: Verify that the modified value is correct according to the matrix mode
          x,y=self.extract_position(modif_cell)
          x=(x+1)%self.line_size
          if(x==0):
               y=(y+1)%self.line_size
          self.move_to(x,y)


     def action_go_up(self) -> None:
          x,y=self.get_currently_focused_position()
          y=(y-1)%self.line_size
          self.move_to(x, y)

     def action_go_down(self) -> None:
          x,y=self.get_currently_focused_position()
          #This will work fine because python uses floored division
          y=(y+1)%self.line_size
          self.move_to(x, y)

     def action_go_right(self) -> None:
          x,y=self.get_currently_focused_position()
          x=(x+1)%self.line_size
          self.move_to(x, y)

     def action_go_left(self) -> None:
          x,y=self.get_currently_focused_position()
          #This will work fine because python uses floored division
          x=(x-1)%self.line_size
          self.move_to(x, y)

     def query_cell(self, x: int, y:int) -> Cell:
          return self.query_one(f"#cell_{x}_{y}", Cell)
     
     def action_clear(self) -> None:
               for cell in self.query("Cell").results(Cell):
                     cell.digit=" "
                     cell.remove_class("correct", "error", "no_state", update=True)

     def __init__(self, m_size : int, *children: Widget, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
          super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)
          self.m_size=m_size
          self.line_size=m_size**2
          self.styles.grid_size_rows=self.line_size
          self.styles.grid_size_columns=self.line_size

     def on_mount(self) -> ComposeResult:
          self.mount_all(Cell(" ", id=f"cell_{x}_{y}") for y in range(self.line_size) for x in range(self.line_size))