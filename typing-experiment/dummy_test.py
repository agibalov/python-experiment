from mypy_extensions import TypedDict


class User(TypedDict):
    id: str
    name: str
    age: int


# error: Function is missing a type annotation
def print_user1(user):
    print('user {}'.format(user))


# error: Function is missing a type annotation for one or more arguments
def print_user2(user) -> None:
    print('user {}'.format(user))


# OK
def print_user3(user: User) -> None:
    print('user {}'.format(user))


def test_typed_dict() -> None:
    # error: Incompatible types (expression has type "int", TypedDict item "id" has type "str")
    user = User(id=123, name='Andrey', age=100)
    assert user == {
        'id': '123',
        'name': 'Andrey',
        'age': 100
    }


def test_print_user3() -> None:
    # error: Argument 1 to "print_user3" has incompatible type "int"; expected "User"
    print_user3(123)

    # OK
    print_user3({'id': 'xxx', 'name': 'Andrey', 'age': 100})

    # error: Extra key 'something' for TypedDict "User"
    print_user3({'id': 'xxx', 'name': 'Andrey', 'something': 100})

    # error: Key 'age' missing for TypedDict "User"
    print_user3({'id': 'xxx', 'name': 'Andrey'})


def test_dummy() -> None:
    a = 'hello'
    b = 123

    # error: Unsupported operand types for + ("str" and "int")
    c = a + b
