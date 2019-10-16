from dataclasses import dataclass, field
from enum import Enum

from dataclasses_json import dataclass_json, config


class Role(Enum):
    Manager = 1
    Developer = 2


@dataclass_json
@dataclass
class Person:
    name: str
    age: int
    role: Role = field(metadata=config(
        encoder=lambda m: m.name,
        decoder=lambda s: Role[s]))


def test_object_to_json():
    assert Person(
        name='Andrey',
        age=100,
        role=Role.Developer).to_json() == '{"name": "Andrey", "age": 100, "role": "Developer"}'


def test_object_from_json():
    assert Person.from_json('{"name": "John", "age": 123, "role": "Developer"}') == Person(
        name='John',
        age=123,
        role=Role.Developer)


def test_object_to_dictionary():
    assert Person.to_dict(Person(name='John', age=123, role=Role.Developer)) == {
        'name': 'John',
        'age': 123,
        'role': 'Developer'
    }


def test_object_from_dictionary():
    assert Person.from_dict({
        'name': 'John',
        'age': 123,
        'role': 'Developer'
    }) == Person(name='John', age=123, role=Role.Developer)
