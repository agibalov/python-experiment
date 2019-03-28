def test_args():
    def f(*args):
        return args

    result = f('hello', 123)
    assert result == ('hello', 123)


def test_kwargs():
    def f(**kwargs):
        return kwargs

    result = f(one='hello', two=123)
    assert result == {
        'one': 'hello',
        'two': 123
    }


def test_args_and_kwargs():
    def f(*args, **kwargs):
        return {
            'args': args,
            'kwargs': kwargs
        }

    result = f('hello', 111, world='!!!', xxx=123)
    assert result == {
        'args': ('hello', 111),
        'kwargs': {
            'world': '!!!',
            'xxx': 123
        }
    }


def test_args_kwargs_and_explicit():
    def f(a, b='default', c='something', *args, **kwargs):
        return {
            'a': a,
            'b': b,
            'c': c,
            'args': args,
            'kwargs': kwargs
        }

    assert f('hello') == {
        'a': 'hello',
        'b': 'default',
        'c': 'something',
        'args': (),
        'kwargs': {}
    }

    assert f('hello', c='qwerty') == {
        'a': 'hello',
        'b': 'default',
        'c': 'qwerty',
        'args': (),
        'kwargs': {}
    }

    assert f('hello', 'bbb', 'ccc', 'ddd') == {
        'a': 'hello',
        'b': 'bbb',
        'c': 'ccc',
        'args': ('ddd',),
        'kwargs': {}
    }

    assert f('hello', omg=123) == {
        'a': 'hello',
        'b': 'default',
        'c': 'something',
        'args': (),
        'kwargs': {
            'omg': 123
        }
    }

    assert f('hello', 'bbb', 'ccc', 'ddd', omg=123) == {
        'a': 'hello',
        'b': 'bbb',
        'c': 'ccc',
        'args': ('ddd',),
        'kwargs': {
            'omg': 123
        }
    }


def test_asterisk_args_call():
    def f(a, b):
        return a, b
    x = (2, 3)
    assert f(2, 3) == (2, 3)
    assert f(*x) == (2, 3)


def test_double_asterisk_kwargs_call():
    def f(a='aaa', b='bbb', c='ccc'):
        return {
            'a': a,
            'b': b,
            'c': c
        }
    x = {
        'b': 'xxx',
        'c': 'yyy'
    }
    assert f(**x) == {
        'a': 'aaa',
        'b': 'xxx',
        'c': 'yyy'
    }


def test_chaining():
    def base(*args, **kwargs):
        return {
            'args': args,
            'kwargs': kwargs
        }

    def f(x, *args, **kwargs):
        return {
            'x': x,
            'args': args,
            'kwargs': kwargs,
            'base': base(*args, **kwargs)
        }

    assert f(111, 222, xxx=333) == {
        'x': 111,
        'args': (222,),
        'kwargs': {
            'xxx': 333
        },
        'base': {
            'args': (222,),
            'kwargs': {
                'xxx': 333
            }
        }
    }
