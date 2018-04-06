from table_flask.helpers import add


def test_add1():
    assert add(1, 2) == 3


def test_add2():
    assert add(0, 2) == 3
