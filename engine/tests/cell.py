from .._cell import Cell


def test_create_cell():
    c = Cell(1, 2)
    assert c
    assert c.row == 1
    assert c.col == 2
