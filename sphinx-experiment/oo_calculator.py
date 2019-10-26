"""This is the OO calculator module.

It provides comprehensive object-oriented APIs to perform advanced numeric computations like
addition, subtraction and even multiplication. Division as well.
"""


class Calculator:
    """This is the Calculator.

    It exposes the calculation functionality.
    """
    def add_numbers(a: int, b: int) -> int:
        """This method adds numbers.

        It takes ``a``, it takes ``b``, and calculates ``a + b``. Then it returns the result.

        :param a: number A.
        :type a: int.
        :param b: number B.
        :type b: int.
        :returns: the sum of number A and number B.
        """
        return a + b

    def sub_numbers(a: int, b: int) -> int:
        """This method subtracts numbers.

        It takes ``a``, it takes ``b``, and calculates ``a - b``. Then it returns the result.

        :param a: number A.
        :type a: int.
        :param b: number B.
        :type b: int.
        :returns: the difference of number A and number B.
        """
        return a - b

    def mul_numbers(a: int, b: int) -> int:
        """This method multiplies numbers.

        It takes ``a``, it takes ``b``, and calculates ``a * b``. Then it returns the result.

        :param a: number A.
        :type a: int.
        :param b: number B.
        :type b: int.
        :returns: the product of number A and number B.
        """
        return a * b

    def div_numbers(a: int, b: int) -> int:
        """This method divides numbers.

        It takes ``a``, it takes ``b``, and calculates ``a / b``. Then it returns the result.

        :param a: number A.
        :type a: int.
        :param b: number B.
        :type b: int.
        :returns: the quotient of number A and number B.
        """
        return a / b
