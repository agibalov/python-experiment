def add_numbers(a, b):
    return a + b


def sub_numbers(a, b):
    return a - b


def mul_numbers(a, b):
    return a * b


def div_numbers(a, b):
    if b == 0:
        raise DivisionByZeroException
    return a / b


class DivisionByZeroException(Exception):
    pass
