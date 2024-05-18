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

from enum import Enum, auto
from widgets.cell import Cell

from textual.message import Message
from textual import log
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Grid
from textual.widget import Widget
from typing import Iterable, List

class Mode(Enum):
     """Indicates the current sudoku mode being used.
     
          ACTIVE Mode will always look up and report errors and correct answers. (AKA: Play)
     
          STATIC Mode is used for inserting cells without checking if it is a valid sudoku (AKA: Resolve)"""
     ACTIVE=auto()
     STATIC=auto()


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
     

     #Not to be confused with Cell.Modified
     class Modified(Message):
          def __init__(self, cell : Cell) -> None:
                 self.cell=cell
                 super().__init__()


     def to_iterable(self) -> Iterable[Iterable[str]]:
          for y in range(self.line_size):
                    yield (cell.digit for cell in (self.query_one(f"#cell_{x}_{y}", Cell) for x in range(self.line_size)))

     def to_list(self) -> List[List[str]]:
           """Creates a list of lists (Matrix) that represents the grid."""
           return [list(x) for x in self.to_iterable()]


     def set_mode_and_clear(self, mode : Mode) -> None:
          self.mode=mode
          self._clear()
     
     
     def clear_and_load(self, mode : Mode, matrix : List[List[str]]) -> None:
          self.set_mode_and_clear(mode)
          self._load(matrix)

     def number_of_correct_cells(self) -> int:
           return len(self.query("Cell.correct"))
     
     
     def number_of_error_cells(self) -> int:
           return len(self.query("Cell.error"))
     
     
     def number_of_no_state_cells(self) -> int:
           return len(self.query("Cell.no_state"))
     
     
     def total_cells(self) -> int:
           return len(self.query("Cell"))
     

     def move_to(self, x: int, y:int) -> None:
          """Sets the focus to the cell at x y position"""
          self.query_one(f"#cell_{x}_{y}",Cell).focus()


     def _extract_position(self, cell : Cell) -> tuple[int, int]:
          """Extracts x and y coordinates from a cell"""
          if(cell.id is not None):
               s=cell.id.split("_", maxsplit=3)
               return (int(s[1]), int(s[2]))
          #TODO: Add proper exception handling
          return (-1,-1)
     

     def _get_currently_focused_position(self) -> tuple[int, int]:
          return self._extract_position(self._get_currently_focused())
     
     def _get_currently_focused(self) -> Cell:
          return self.query_one("Cell:focus", Cell)
     

     @on(Cell.Modified)
     def modified(self, modified : Cell.Modified) -> None:
          """Handles cell modifications, may add one of the following classes to the modified cell:
     
     correct if the answer was correct.
     
     error if the guess was incorrect because it doesn't respect the rules of sudoku.     
     
     no_state if the user has inserted an answer but it wasn't checked if it respects the rules of sudoku or that the answer was deleted"""
          log.debug(self.to_list())
          modif_cell=self.query_one("#"+modified.id, Cell)
          if(self.mode is Mode.STATIC):
                return
          if(modif_cell.digit==" "):
               modif_cell.remove_class("error", update=True)
               modif_cell.add_class("no_state", update=True)
               self.post_message(self.Modified(modif_cell))
               return
          x,y=self._extract_position(modif_cell)
          #Note: the modif_cell.has_class("correct")==True case is skipped because it is handled by the cell class itself
          if(self.is_correct(x,y)):
                modif_cell.add_class("correct", update=True)
                modif_cell.remove_class("error", update=True)
                modif_cell.remove_class("no_state", update=True)
                self.post_message(self.Modified(modif_cell))
          else:
                modif_cell.remove_class("no_state", update=True)
                modif_cell.add_class("error", update=True)
                self.post_message(self.Modified(modif_cell))
          

     def is_correct(self, x:int, y:int) -> None:
           """Placeholder function"""
           pass
     

     def move_forward(self, cell : Cell) -> None:
          x,y=self._extract_position(cell)
          x=(x+1)%self.line_size
          if(x==0):
               y=(y+1)%self.line_size
          self.move_to(x,y)


     def action_go_up(self) -> None:
          x,y=self._get_currently_focused_position()
          y=(y-1)%self.line_size
          self.move_to(x, y)


     def action_go_down(self) -> None:
          x,y=self._get_currently_focused_position()
          #This will work fine because python uses floored division
          y=(y+1)%self.line_size
          self.move_to(x, y)


     def action_go_right(self) -> None:
          x,y=self._get_currently_focused_position()
          x=(x+1)%self.line_size
          self.move_to(x, y)


     def action_go_left(self) -> None:
          x,y=self._get_currently_focused_position()
          #This will work fine because python uses floored division
          x=(x-1)%self.line_size
          self.move_to(x, y)


     def query_cell(self, x: int, y:int) -> Cell:
          return self.query_one(f"#cell_{x}_{y}", Cell)
     
     
     def _clear(self) -> None:
               for cell in self.query("Cell").results(Cell):
                     cell.digit=" "
                     cell.remove_class("correct", "error", "no_state", update=True)

     
     def _load(self, matrix : List[List[str]]) -> None:
           if(self.mode is Mode.STATIC):
                 class_str="no_state"
           else:
                 #hint is only used when loading from an external matrix in ACTIVE mode
                 class_str=["correct", "hint"]
           for x in range(self.line_size):
                 for y in range(self.line_size):
                       cell=self.query_cell(x,y)
                       cell.digit=matrix[x][y]
                       cell.add_class(*class_str, update=True)


     def __init__(self, size : int, mode : Mode = Mode.STATIC, *children: Widget, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
          super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)
          self.m_size=size
          self.line_size=self.m_size**2
          self.styles.grid_size_rows=self.line_size
          self.styles.grid_size_columns=self.line_size
          self.mode=mode


     def compose(self) -> ComposeResult:
           for y in range(self.line_size):
                 for x in range(self.line_size):
                       yield Cell(" ", id=f"cell_{x}_{y}")