def test_default():
    class X:
        pass

    x = X()
    assert str(x).startswith('<str_and_repr_test.test_default.<locals>.X object at ')
    assert '{}'.format(x) == str(x)
    assert repr(x) == str(x)


def test_custom_str():
    class X:
        def __str__(self):
            return 'qwerty'

    x = X()
    assert str(x) == 'qwerty'
    assert '{}'.format(x) == str(x)
    assert repr(x).startswith('<str_and_repr_test.test_custom_str.<locals>.X object at ')
