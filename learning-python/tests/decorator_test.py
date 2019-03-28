from unittest.mock import Mock, call


def test_decorate_function():
    mock = Mock()

    def decorate(func):
        def wrapper(*args, **kwargs):
            mock.before(*args, **kwargs)
            result = func(*args, **kwargs)
            mock.after(*args, **kwargs)
            return result
        return wrapper

    @decorate
    def my_func(s):
        mock.hello(s)

    my_func('hi')

    assert mock.method_calls == [
        call.before('hi'),
        call.hello('hi'),
        call.after('hi')
    ]
