import alembic
import sqlalchemy

revision = '1'
down_revision = None
branch_labels = None


def upgrade():
    alembic.op.create_table(
        'AlembicUsers',
        sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column('name', sqlalchemy.String)
    )
