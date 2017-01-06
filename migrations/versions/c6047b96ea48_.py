"""empty message

Revision ID: c6047b96ea48
Revises: 581b4fdfe692
Create Date: 2016-12-28 00:40:40.984014

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6047b96ea48'
down_revision = '581b4fdfe692'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sample', sa.Column('sample_type_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'sample', 'SampleType', ['sample_type_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'sample', type_='foreignkey')
    op.drop_column('sample', 'sample_type_id')
    # ### end Alembic commands ###
