x: 'hello'


def test_use_local_variable_annotations():
    y: 'qwerty' = 123  # TODO: how do I get y's annotation?
    assert __annotations__ == {
        'x': 'hello'
    }


def test_use_function_annotations():
    something = 'hello'

    def f(a: something, b: 'world', c: (lambda: 'xxx')()) -> 'omg':
        pass

    assert f.__annotations__ == {
        'a': 'hello',
        'b': 'world',
        'c': 'xxx',
        'return': 'omg'
    }


def test_use_class_annotations():
    class X:
        a: 'hello'

        def f(self: 'qqq', b: 'www') -> 'eee':
            pass
    assert X.__annotations__ == {
        'a': 'hello'
    }
    assert X.f.__annotations__ == {
        'self': 'qqq',
        'b': 'www',
        'return': 'eee'
    }
