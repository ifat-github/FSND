"""empty message

Revision ID: f4da1964fc1e
Revises: 9b734e232c2f
Create Date: 2021-04-16 19:35:37.329296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4da1964fc1e'
down_revision = '9b734e232c2f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'past_shows')
    op.drop_column('Artist', 'past_shows_count')
    op.drop_column('Artist', 'upcoming_shows_count')
    op.drop_column('Artist', 'upcoming_shows')
    op.add_column('Venue', sa.Column('genres', sa.String(length=120), nullable=True))
    op.drop_column('Venue', 'past_shows')
    op.drop_column('Venue', 'past_shows_count')
    op.drop_column('Venue', 'upcoming_shows_count')
    op.drop_column('Venue', 'upcoming_shows')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('upcoming_shows', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.add_column('Venue', sa.Column('upcoming_shows_count', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('Venue', sa.Column('past_shows_count', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('Venue', sa.Column('past_shows', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.drop_column('Venue', 'genres')
    op.add_column('Artist', sa.Column('upcoming_shows', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.add_column('Artist', sa.Column('upcoming_shows_count', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('Artist', sa.Column('past_shows_count', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('Artist', sa.Column('past_shows', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    # ### end Alembic commands ###