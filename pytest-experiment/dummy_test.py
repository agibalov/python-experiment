from calculator import add_numbers, sub_numbers, div_numbers


def test_add_numbers():
    assert add_numbers(2, 3) == 5


def test_sub_numbers():
    assert sub_numbers(2, 3) == -1


def test_div_numbers():
    assert div_numbers(10, 2) == 5
