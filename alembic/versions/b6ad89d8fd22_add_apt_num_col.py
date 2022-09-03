"""add apt num col

Revision ID: b6ad89d8fd22
Revises: 9c40f5c634e6
Create Date: 2022-09-03 09:44:32.558541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6ad89d8fd22'
down_revision = '9c40f5c634e6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('address', sa.Column('apt_num', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('address', 'apt_num')
