import pytest
from sqlalchemy import String, Column, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound


def test():
    Base = declarative_base()

    class Note(Base):
        __tablename__ = 'notes'
        id = Column(String, primary_key=True)
        text = Column(String)

    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    session = Session()
    try:
        note = Note(id='note1', text='Note one')
        session.add(note)
        session.commit()
    finally:
        session.close()

    session = Session()
    try:
        note1 = session.query(Note).filter(Note.id == 'note1').one()
        assert note1.id == 'note1'
        assert note1.text == 'Note one'

        note1 = session.query(Note).filter(text('id = :id')).params(id='note1').one()
        assert note1.id == 'note1'
        assert note1.text == 'Note one'

        note1 = session.query(Note).from_statement(
            text('select id, text from notes where id = :id')
        ).params(id='note1').one()
        assert note1.id == 'note1'
        assert note1.text == 'Note one'

        try:
            session.query(Note).filter(Note.id == 'note2').one()
            pytest.fail('Should throw')
        except NoResultFound:
            pass

        note2 = session.query(Note).filter(Note.id == 'note2').one_or_none()
        assert note2 is None
    finally:
        session.close()

    session = Session()
    try:
        note1 = session.query(Note).filter(Note.id == 'note1').one()
        note1.text = 'hello there'

        note2 = Note(id='note2', text='Note two')
        session.add(note2)

        assert note1 in session.dirty
        assert note2 in session.new
        assert len(session.deleted) == 0
    finally:
        session.close()
