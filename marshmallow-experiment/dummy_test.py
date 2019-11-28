from dataclasses import dataclass

from marshmallow import Schema, fields, post_load, validate, ValidationError


def test_can_serialize_diry_dict_to_dict():
    class NoteSchema(Schema):
        id = fields.Str()
        text = fields.Str()
        priority = fields.Int()

    note_schema = NoteSchema()
    assert note_schema.dump({
        'id': 123,
        'text': 'hello world',
        'priority': '3'
    }) == {
        'id': '123',
        'text': 'hello world',
        'priority': 3
    }


def test_can_serialize_dataclass_to_dict():
    class NoteSchema(Schema):
        id = fields.Str()
        text = fields.Str()
        priority = fields.Int()

    @dataclass
    class Note:
        id: str
        text: str
        priority: int

    note_schema = NoteSchema()
    assert note_schema.dump(Note(id='123', text='hello world', priority=3)) == {
        'id': '123',
        'text': 'hello world',
        'priority': 3
    }


def test_can_deserialize_dict_from_dict():
    class NoteSchema(Schema):
        id = fields.Str()
        text = fields.Str()
        priority = fields.Int()

    note_schema = NoteSchema()
    assert note_schema.load({
        'id': '123',
        'text': 'hello world',
        'priority': 3
    }) == {'id': '123', 'text': 'hello world', 'priority': 3}


def test_can_deserialize_dataclass_from_dict():
    class NoteSchema(Schema):
        id = fields.Str()
        text = fields.Str()
        priority = fields.Int()

        @post_load
        def make_note(self, data, **kwargs):
            return Note(**data)

    @dataclass
    class Note:
        id: str
        text: str
        priority: int

    note_schema = NoteSchema()
    assert note_schema.load({
        'id': '123',
        'text': 'hello world',
        'priority': 3
    }) == Note(id='123', text='hello world', priority=3)


def test_can_validate():
    def validate_priority(p):
        if p < 0:
            raise ValidationError('Priority must be > 0')
        if p > 3:
            raise ValidationError('Priority must be <= 3')

    class NoteSchema(Schema):
        id = fields.Str(required=True)
        text = fields.Str(required=True, validate=validate.Length(min=10))
        priority = fields.Int(required=True, validate=validate_priority)

    assert NoteSchema().validate({
        'text': 'hello',
        'priority': 20
    }) == {
        'text': ['Shorter than minimum length 10.'],
        'priority': ['Priority must be <= 3'],
        'id': ['Missing data for required field.']
    }

    assert NoteSchema().validate({
        'id': '123',
        'text': 'hello world',
        'priority': 3
    }) == {}
