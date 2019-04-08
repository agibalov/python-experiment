from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Person:
    name: str
    age: int


def test_object_to_json():
    assert Person(name='Andrey', age=100).to_json() == '{"name": "Andrey", "age": 100}'


def test_object_from_json():
    assert Person.from_json('{"name": "John", "age": 123}') == Person(name='John', age=123)


def test_object_to_dictionary():
    assert Person.schema().dump(Person(name='John', age=123)) == {
        'name': 'John',
        'age': 123
    }


def test_object_from_dictionary():
    assert Person.schema().load({
        'name': 'John',
        'age': 123
    }) == Person(name='John', age=123)
