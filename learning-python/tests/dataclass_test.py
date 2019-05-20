from dataclasses import dataclass, asdict, field
from typing import List


def test_dataclass():
    @dataclass
    class Person:
        name: str
        age: int

    person = Person(name='Andrey', age=100)
    assert person.name == 'Andrey'
    assert person.age == 100
    assert str(person) == "test_dataclass.<locals>.Person(name='Andrey', age=100)"
    assert asdict(person) == {
        'name': 'Andrey',
        'age': 100
    }


def test_dataclass_field():
    @dataclass
    class Person:
        name: str
        age: int = field(repr=False)

    person = Person(name='Andrey', age=100)
    assert str(person) == "test_dataclass_field.<locals>.Person(name='Andrey')"


def test_dataclass_nested():
    @dataclass
    class Interest:
        description: str

    @dataclass
    class Person:
        name: str
        interests: List[Interest]

    person = Person(name='Andrey', interests=[Interest(description='cats')])
    assert asdict(person) == {
        'name': 'Andrey',
        'interests': [{'description': 'cats'}]
    }
