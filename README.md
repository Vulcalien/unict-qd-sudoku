# Sudoku TUI
Play Sudoku on your Terminal.

This is an implementation of the game
[Sudoku](https://en.wikipedia.org/wiki/Sudoku)
that makes use of a Terminal User Interface (TUI) and generates all
puzzles locally.

## How to run
To run the game, first install the Python dependencies by running this
command:
```sh
pip install textual
```

Then, run `./sudoku-tui` (on Unix-like systems) or `sudoku-tui` (on
Windows).

## How to play
After starting the game, press 'Play' to generate a new puzzle. This may
take a few seconds.

You'll then see a 9x9 Sudoku grid with hints and empty cells. The given
puzzle has only one solution: to win the game, you must guess the value
of all hidden cells.

Use the mouse, 'WASD' keys or arrow keys to move around the grid. Write
numbers between 1 and 9 to empty cells. If the cell becomes green, then
the guess was correct. If the cell becomes red, you'll need to take
another guess.

If you don't like the puzzle that was generated, press 'R' to generate a
new one.

### Sudoku rules
A full Sudoku grid must have, for each row, column and 3x3 square, the
full set of symbols from 1 to 9. This means that, for example, the
symbol '1' cannot be present twice in a single row.

## License and Authors
This program is free software licensed under the GNU General Public
License, version 3 or later.

Made by Henrysk and Vulcalien for the 2023-2024 Quality Development
course at *Università di Catania*.
