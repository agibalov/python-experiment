import functools
import time


def test_decorate_function():
    log = []

    def trace(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            log.append('before')
            start_time = time.perf_counter()
            result = None
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                elapsed_time = time.perf_counter() - start_time
                print(f'{func.__module__}::{func.__name__} time={elapsed_time:.3f} args={args} kwargs={kwargs} result={result}')
                log.append('after')
        return wrapper

    @trace
    def add_numbers(a, b):
        log.append('add_numbers')
        time.sleep(0.1)
        return a + b

    assert add_numbers.__name__ == 'add_numbers'

    add_numbers(2, 3)

    assert log == ['before', 'add_numbers', 'after']
