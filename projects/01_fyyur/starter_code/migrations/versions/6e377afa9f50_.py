"""empty message

Revision ID: 6e377afa9f50
Revises: 909d6808678b
Create Date: 2021-04-21 11:37:24.570598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e377afa9f50'
down_revision = '909d6808678b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Show', 'id')
    # ### end Alembic commands ###
