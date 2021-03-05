"""Relarionship

Revision ID: 16de3bb73daf
Revises: af70c37b305c
Create Date: 2021-03-04 20:44:39.605302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16de3bb73daf'
down_revision = 'af70c37b305c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('timer', sa.Column('username', sa.String(length=50), nullable=True))
    op.add_column('todos', sa.Column('username', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todos', 'username')
    op.drop_column('timer', 'username')
    # ### end Alembic commands ###