from unittest.mock import Mock, call


def test_with():
    mock = Mock()

    class Resource:
        def __enter__(self):
            mock.enter()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            mock.exit()

        def work(self):
            mock.do_something()

    with Resource() as r:
        r.work()

    assert mock.method_calls == [
        call.enter(),
        call.do_something(),
        call.exit()
    ]