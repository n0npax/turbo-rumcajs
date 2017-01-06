"""empty message

Revision ID: e630dba991ff
Revises: ac71ff518f4b
Create Date: 2016-12-27 23:00:58.845656

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e630dba991ff'
down_revision = 'ac71ff518f4b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('datasample_type_settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('datasample_type_settings')
    # ### end Alembic commands ###
