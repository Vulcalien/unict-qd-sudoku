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

import os
import sys

import pytest
import logging

from src.app.app import SudokuApp
from src.app.widgets.play import Play # type: ignore
from src.app.widgets.matrix import Matrix # type: ignore

LOGGER = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_push_screen():
    app=SudokuApp()
    async with app.run_test() as pilot:
        await pilot.click("#playb")
        await pilot.pause()
        assert isinstance(app.screen, Play)


@pytest.mark.asyncio
async def test_play_correct():
    app=SudokuApp()
    if os.name=="nt": #Checks if we are using Windows NT
        width=210
        height=55
    else:
        width=193
        height=50
    async with app.run_test(size=(width,height)) as pilot:
        await pilot.click("#playb")
        await pilot.pause()
        m : Matrix = app.screen.query_one("Matrix", Matrix)
        app.screen.focus()
        for current_cell in m._get_no_state_cells():
            i,j=m._extract_position(current_cell)
            logging.info(f"Current Cordinates: ({i=} {j=})")
            assert i!=-1 and j!=-1
            if os.name=="nt":
                await pilot.click(f".cell_{i}_{j}")
            else: 
                current_cell.focus()
            correct_answer=str(m._sudoku.get_cell(j,i))
            await pilot.press(correct_answer)
            await pilot.pause()
            assert "correct" in current_cell.classes
            assert current_cell.digit == str(m._sudoku.get_cell(j,i))
        assert m.number_of_correct_cells() == m.total_cells() # Check the matrix state
