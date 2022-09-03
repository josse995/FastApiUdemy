"""Create address table

Revision ID: e8a992b732b4
Revises: a52f194a4901
Create Date: 2022-09-03 09:17:37.472754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8a992b732b4'
down_revision = 'a52f194a4901'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('address',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('address1', sa.String(), nullable=False),
                    sa.Column('address2', sa.String(), nullable=False),
                    sa.Column('city', sa.String(), nullable=False),
                    sa.Column('state', sa.String(), nullable=False),
                    sa.Column('country', sa.String(), nullable=False),
                    sa.Column('postalcode', sa.String(), nullable=False),
                    )


def downgrade():
    op.drop_table('address')
