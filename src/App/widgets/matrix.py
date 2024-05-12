from src.App.widgets.cell import Cell

from textual import log
from textual import on
from textual.events import DescendantBlur, Blur
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Grid
from textual.widget import Widget


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
          ]
     

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

     def __init__(self, m_size : int, *children: Widget, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
          super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)
          self.m_size=m_size
          self.line_size=m_size**2
          self.styles.grid_size_rows=self.line_size
          self.styles.grid_size_columns=self.line_size

     def on_mount(self) -> ComposeResult:
          #Oggi offre l'haskeller
          self.mount_all(Cell(" ", id=f"cell_{x}_{y}") for y in range(self.line_size) for x in range(self.line_size))