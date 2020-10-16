from .._point import Point


def test_create_point():
    p = Point(1, 2)
    assert p
    assert p.x == 1
    assert p.y == 2
    assert p.z == 0

    p = Point(3, 4, 1)
    assert p
    assert p.x == 3
    assert p.y == 4
    assert p.z == 1

    p = Point()
    assert p
    assert p.x == 0
    assert p.y == 0
    assert p.z == 0


def test_get_point():
    p = Point(5, 6)
    assert p.get() == (5, 6)
    assert p.zget() == (5, 6, 0)


def test_set_point():
    p = Point()
    p.set(10)
    assert p.zget() == (10, 0, 0)
    p.set(y=11)
    assert p.zget() == (10, 11, 0)
    p.set(z=2)
    assert p.zget() == (10, 11, 2)


def test_incr_point():
    p = Point()
    p.incr(1)
    assert p.zget() == (1, 0, 0)
    p.incr(y=1)
    assert p.zget() == (1, 1, 0)
    p.incr(z=1)
    assert p.zget() == (1, 1, 1)


def test_decr_point():
    p = Point(10, 20, 5)
    p.decr(10)
    assert p.zget() == (0, 20, 5)
    p.decr(y=10)
    assert p.zget() == (0, 10, 5)
    p.decr(z=1)
    assert p.zget() == (0, 10, 4)


def test_add_point():
    p = Point(1, 1, 2)
    p = p + Point(1, 2, 1)
    assert p.zget() == (2, 3, 3)
    p = p + 10
    assert p.zget() == (12, 13, 3)


def test_sub_point():
    p = Point(10, 20, 5)
    p = p - Point(1, 2, 1)
    assert p.zget() == (9, 18, 4)
    p = p - 5
    assert p.zget() == (4, 13, 4)


def test_mul_point():
    p = Point(1, 2, 2)
    p = p * Point(2, 3, 5)
    assert p.zget() == (2, 6, 2)
    p = p * 2
    assert p.zget() == (4, 12, 2)


def test_eq_point():
    p = Point(1, 2, 1)
    assert p == Point(1, 2, 1)
    assert p != Point(0, 2, 1)
    assert p != Point(1, 0, 1)
    assert p != Point(1, 2, 0)


def tets_clone_point():
    p = Point(1, 2, 3)
    new_p = p.clone()
    assert new_p
    assert new_p.zget() == (1, 2, 3)


def test_inside_point():
    p = Point(2, 2)
    assert p.inside(0, 0, 3, 3)
    assert not p.inside(3, 3, 1, 1)
