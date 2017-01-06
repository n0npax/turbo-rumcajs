"""empty message

Revision ID: 5e4d8dbd1466
Revises: a10f19a3b460
Create Date: 2016-12-27 23:53:09.076463

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5e4d8dbd1466'
down_revision = 'a10f19a3b460'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('SampleTypeSettings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sample',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('sample', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('SampleType',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('sample_type_settings_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sample_type_settings_id'], ['SampleTypeSettings.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('datasample')
    op.drop_table('sample_type')
    op.drop_table('sample_type_settings')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sample_type_settings',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('sample_type_settings_id_seq'::regclass)"), nullable=False),
    sa.PrimaryKeyConstraint('id', name='sample_type_settings_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('sample_type',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('sample_type_id_seq'::regclass)"), nullable=False),
    sa.Column('sample_type_settings_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['sample_type_settings_id'], ['sample_type_settings.id'], name='sample_type_sample_type_settings_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='sample_type_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('datasample',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('sample', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('sample_type_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['sample_type_id'], ['sample_type.id'], name='datasample_sample_type_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='datasample_pkey')
    )
    op.drop_table('SampleType')
    op.drop_table('sample')
    op.drop_table('SampleTypeSettings')
    # ### end Alembic commands ###