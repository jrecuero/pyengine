from .._size import Size


def test_create_size():
    s = Size(10, 20)
    assert s
    assert s.x == 10
    assert s.y == 20
    assert s.halfx == 5
    assert s.halfy == 10
    assert s.half == (5, 10)


def test_in_size():
    s = Size(10, 20)
    assert s.in_x(0)
    assert s.in_x(9)
    assert s.in_x(10) is False
    assert s.in_x(-1) is False
    assert s.in_y(0)
    assert s.in_y(19)
    assert s.in_y(20) is False
    assert s.in_y(-1) is False
    assert s.in_size(0, 0)
    assert s.in_size(9, 0)
    assert s.in_size(9, 19)
    assert s.in_size(10, 0) is False
    assert s.in_size(0, 20) is False
    assert s.in_size(10, 20) is False
    assert s.in_size(-1, 0) is False
    assert s.in_size(0, -1) is False
