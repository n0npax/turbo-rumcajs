"""empty message

Revision ID: e69a72eaf8b7
Revises: 049b9555e2c0
Create Date: 2017-01-14 17:47:24.327898

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e69a72eaf8b7'
down_revision = '049b9555e2c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.Column('is_enabled', sa.Boolean(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('university', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.alter_column('sample_settings', 'alpha',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('sample_settings', 'k',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('sample_settings', 'mi',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('sample_settings', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('sample_settings', 'prefix_x',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('sample_settings', 'prefix_y',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('sample_settings', 'solution_at_x',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('sample_settings', 'solution_at_y',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sample_settings', 'solution_at_y',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('sample_settings', 'solution_at_x',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('sample_settings', 'prefix_y',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('sample_settings', 'prefix_x',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('sample_settings', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('sample_settings', 'mi',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('sample_settings', 'k',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('sample_settings', 'alpha',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.drop_table('user')
    # ### end Alembic commands ###