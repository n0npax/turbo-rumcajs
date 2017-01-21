"""empty message

Revision ID: 51749e600e35
Revises: ddb8ebdc4ee2
Create Date: 2017-01-20 22:46:07.932035

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51749e600e35'
down_revision = 'ddb8ebdc4ee2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sample_settings', sa.Column('can_process', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sample_settings', 'can_process')
    # ### end Alembic commands ###