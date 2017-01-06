"""empty message

Revision ID: f788f7a68653
Revises: c6047b96ea48
Create Date: 2016-12-28 00:43:36.302239

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f788f7a68653'
down_revision = 'c6047b96ea48'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Sample',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('sample', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('sample_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sample_type_id'], ['SampleType.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('sample')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sample',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('sample', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('sample_type_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['sample_type_id'], ['SampleType.id'], name='sample_sample_type_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='sample_pkey')
    )
    op.drop_table('Sample')
    # ### end Alembic commands ###