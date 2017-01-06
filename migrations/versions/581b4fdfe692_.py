"""empty message

Revision ID: 581b4fdfe692
Revises: 785c80de9e85
Create Date: 2016-12-28 00:34:05.268045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '581b4fdfe692'
down_revision = '785c80de9e85'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('SampleType', sa.Column('settings_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'SampleType', 'SampleTypeSettings', ['settings_id'], ['id'])
    op.drop_constraint('sample_sample_type_id_fkey', 'sample', type_='foreignkey')
    op.drop_column('sample', 'sample_type_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sample', sa.Column('sample_type_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('sample_sample_type_id_fkey', 'sample', 'SampleType', ['sample_type_id'], ['id'])
    op.drop_constraint(None, 'SampleType', type_='foreignkey')
    op.drop_column('SampleType', 'settings_id')
    # ### end Alembic commands ###
