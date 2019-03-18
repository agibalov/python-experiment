import sqlalchemy
import alembic, alembic.config


def test_alembic_migrations():
    engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=True)

    alembic_config = alembic.config.Config()
    alembic_config.set_main_option('script_location', 'alembic')

    if True:
        with engine.begin() as connection:
            alembic_config.attributes['connection'] = connection
            alembic.command.upgrade(alembic_config, '1')

        metadata = sqlalchemy.MetaData()
        users = sqlalchemy.Table(
            'AlembicUsers',
            metadata,
            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
            sqlalchemy.Column('name', sqlalchemy.String))

        connection = engine.connect()
        connection.execute(users.insert().values(id=123, name='qwerty'))
        rows = connection.execute(sqlalchemy.sql.select([users])).fetchall()
        assert rows == [(123, 'qwerty')]

    if True:
        with engine.begin() as connection:
            alembic_config.attributes['connection'] = connection
            alembic.command.upgrade(alembic_config, '2')

        metadata = sqlalchemy.MetaData()
        users = sqlalchemy.Table(
            'AlembicUsers',
            metadata,
            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
            sqlalchemy.Column('name', sqlalchemy.String),
            sqlalchemy.Column('description', sqlalchemy.String))

        connection = engine.connect()
        rows = connection.execute(sqlalchemy.sql.select([users])).fetchall()
        assert rows == [(123, 'qwerty', 'A dummy description for 123')]


def test_sql_alchemy():
    metadata = sqlalchemy.MetaData()
    users = sqlalchemy.Table(
        'Users',
        metadata,
        sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column('name', sqlalchemy.String))

    engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=True)
    metadata.create_all(engine)

    connection = engine.connect()
    result = connection.execute(users.insert().values(id=123, name='qwerty'))
    assert result.inserted_primary_key == [123]

    connection.execute(users.insert(), [
        {'id': 111, 'name': 'user 111'},
        {'id': 222, 'name': 'user 222'}
    ])

    rows = connection.execute(sqlalchemy.sql.select([users])).fetchall()
    assert rows == [
        (111, 'user 111'),
        (123, 'qwerty'),
        (222, 'user 222')
    ]
