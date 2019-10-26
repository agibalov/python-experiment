"""This is the calculator module.

It provides comprehensive APIs to perform advanced numeric computations like addition,
subtraction and even multiplication. Division as well. Here's what it does in general:

.. literalinclude:: ../calculator_test.py
    :start-after: fun-start
    :end-before: fun-end
"""


# add_numbers_start
def add_numbers(a: int, b: int) -> int:
    """This function adds numbers.

    It takes ``a``, it takes ``b``, and calculates ``a + b``. Then it returns the result.

    :param a: number A.
    :type a: int.
    :param b: number B.
    :type b: int.
    :returns: the sum of number A and number B.

    Here's an example:

    .. literalinclude:: ../calculator_test.py
        :start-after: add-numbers1-start
        :end-before: add-numbers1-end

    Here's another one:

    .. literalinclude:: ../calculator_test.py
        :start-after: add-numbers2-start
        :end-before: add-numbers2-end

    Ha?
    """
    return a + b
# add_numbers_end


def sub_numbers(a: int, b: int) -> int:
    """This function subtracts numbers.

    It takes ``a``, it takes ``b``, and calculates ``a - b``. Then it returns the result.

    :param a: number A.
    :type a: int.
    :param b: number B.
    :type b: int.
    :returns: the difference of number A and number B.

    Here's an example:

    .. literalinclude:: ../calculator_test.py
        :start-after: sub-numbers-start
        :end-before: sub-numbers-end
    """
    return a - b


def mul_numbers(a: int, b: int) -> int:
    """This function multiplies numbers.

    It takes ``a``, it takes ``b``, and calculates ``a * b``. Then it returns the result.

    :param a: number A.
    :type a: int.
    :param b: number B.
    :type b: int.
    :returns: the product of number A and number B.

    Here's an example:

    .. literalinclude:: ../calculator_test.py
        :start-after: mul-numbers-start
        :end-before: mul-numbers-end
    """
    return a * b


def div_numbers(a: int, b: int) -> int:
    """This function divides numbers.

    It takes ``a``, it takes ``b``, and calculates ``a / b``. Then it returns the result.

    :param a: number A.
    :type a: int.
    :param b: number B.
    :type b: int.
    :returns: the quotient of number A and number B.

    Here's an example:

    .. literalinclude:: ../calculator_test.py
        :start-after: div-numbers-start
        :end-before: div-numbers-end
    """
    return a / b
