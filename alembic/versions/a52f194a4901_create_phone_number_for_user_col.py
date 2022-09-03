"""create phone number for user col

Revision ID: a52f194a4901
Revises: 
Create Date: 2022-09-03 09:11:01.754184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a52f194a4901'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade():
    op.drop_column('users', 'phone_number')
