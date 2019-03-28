from enum import Enum


def test_enum():
    class Color(Enum):
        RED = 1
        GREEN = 2
        BLUE = 3

    assert Color.RED == Color.RED
    assert Color.RED != Color.GREEN
    assert Color.RED.value == 1
    assert Color(1) == Color.RED

    assert list(Color) == [
        Color.RED,
        Color.GREEN,
        Color.BLUE
    ]


def test_string_enum():
    class Color(Enum):
        RED = 'red'
        GREEN = 'green'
        BLUE = 'blue'

    assert Color.RED.value == 'red'
    assert Color('red') == Color.RED
