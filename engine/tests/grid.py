from .._point import Point
from .._cell import Cell
from .._size import Size
from .._rect import Rect
from .._grid import Grid


def test_grid_create():
    g = Grid(2, 3, 0, 0, 32, 32)
    assert g
    assert g.rows == 2
    assert g.cols == 3
    assert g.cell_size == Size(32, 32)
    assert g.g_origin == Point(0, 0)
    assert g.g_size == Size(96, 64)
    assert len(g.db) == 2
    assert len(g.db[0]) == 3
    for cell, row, col in [(g.db[row][col], row, col) for col in range(3) for row in range(2)]:
        assert cell
        assert isinstance(cell, Cell)
        assert cell.col == col
        assert cell.row == row


def test_grid_cell():
    g = Grid(2, 3, 0, 0, 32, 32)
    cell = g.cell(1, 2)
    assert cell
    assert cell.col == 2
    assert cell.row == 1


def test_grid_g_cell():
    g = Grid(2, 3, 0, 0, 32, 32)
    g_cell = g.g_cell(1, 2)
    assert g_cell
    assert g_cell.x == 64
    assert g_cell.y == 32


def test_grid_g_cell_rect():
    g = Grid(2, 3, 0, 0, 32, 32)
    r = g.g_cell_rect(1, 2)
    assert r == Rect(64, 32, 32, 32)


def test_grid_grid_rect():
    g = Grid(2, 3, 0, 0, 32, 32)
    r = g.grid_rect()
    assert r == Rect(0, 0, 96, 64)
