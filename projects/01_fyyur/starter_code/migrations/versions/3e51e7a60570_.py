"""empty message

Revision ID: 3e51e7a60570
Revises: f4da1964fc1e
Create Date: 2021-04-16 19:39:36.592950

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e51e7a60570'
down_revision = 'f4da1964fc1e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.drop_column('Venue', 'seeking_venue')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('seeking_venue', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('Venue', 'seeking_talent')
    # ### end Alembic commands ###
