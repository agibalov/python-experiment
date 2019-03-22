import pytest
from unittest.mock import Mock, call


def test_mock_assert_called_throws_when_no_method_call():
    mock = Mock()
    try:
        mock.do_something.assert_called()
    except AssertionError:
        pass
    else:
        pytest.fail()


def test_mock_assert_called_doesnt_throw_when_method_call():
    mock = Mock()
    try:
        mock.do_something.assert_called()
    except AssertionError:
        pass
    else:
        pytest.fail()


def test_various_method_call_assertions():
    mock = Mock()
    mock.do_something(123, 'hello there', xxx=3.14)
    mock.do_something.assert_called()
    mock.do_something.assert_called_once()
    mock.do_something.assert_called_with(123, 'hello there', xxx=3.14)
    mock.do_something.assert_called_once_with(123, 'hello there', xxx=3.14)


def test_call_args():
    mock = Mock()
    mock.do_something(111, 222)
    mock.do_something('hello world')
    mock.do_something(3.14, xxx=222)

    assert mock.do_something.call_args == call(3.14, xxx=222)

    args, kwargs = mock.do_something.call_args
    assert args == (3.14,)
    assert kwargs == {'xxx':222}

    assert mock.do_something.call_args_list == [
        call(111, 222),
        call('hello world'),
        call(3.14, xxx=222)
    ]


def test_configure_mock():
    mock = Mock(x = 123)
    mock.y = 222
    mock.get_greeting.return_value = 'hi there!'
    mock.throw_something.side_effect = Exception('I am side effect')
    assert mock.x == 123
    assert mock.y == 222
    assert mock.get_greeting() == 'hi there!'
    try:
        mock.throw_something()
    except Exception as e:
        assert str(e) == 'I am side effect'
    else:
        pytest.fail()
