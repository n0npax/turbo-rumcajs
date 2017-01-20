"""empty message

Revision ID: 254b0521b4ac
Revises: 51749e600e35
Create Date: 2017-01-20 22:52:17.940959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '254b0521b4ac'
down_revision = '51749e600e35'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sample_settings', sa.Column('need_process', sa.Boolean(), nullable=True))
    op.drop_column('sample_settings', 'can_process')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sample_settings', sa.Column('can_process', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('sample_settings', 'need_process')
    # ### end Alembic commands ###
