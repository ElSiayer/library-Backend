"""Add rating book

Revision ID: d492b34d93a5
Revises: 
Create Date: 2022-03-09 17:52:31.283434

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd492b34d93a5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('book', sa.Column('rating', sa.Integer))



def downgrade():
    op.drop_column('book','rating')
