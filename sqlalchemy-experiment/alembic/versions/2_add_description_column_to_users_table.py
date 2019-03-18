import alembic
import sqlalchemy

revision = '2'
down_revision = '1'
branch_labels = None


def upgrade():
    alembic.op.add_column(
        'AlembicUsers',
        sqlalchemy.Column('description', sqlalchemy.String)
    )
    alembic.op.get_bind().execute(
        'update AlembicUsers set description = :description_prefix || id',
        description_prefix='A dummy description for '
    )
