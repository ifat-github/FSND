"""empty message

Revision ID: 4247986676f2
Revises: 593f9b9affe8
Create Date: 2021-04-17 23:04:31.500595

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4247986676f2'
down_revision = '593f9b9affe8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('id', sa.Integer(), nullable=False))
    op.alter_column('Show', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Show', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Show', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('Show', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('Show', 'id')
    # ### end Alembic commands ###
