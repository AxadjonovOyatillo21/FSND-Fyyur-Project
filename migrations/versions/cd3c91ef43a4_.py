"""empty message

Revision ID: cd3c91ef43a4
Revises: 
Create Date: 2021-05-18 18:24:22.470322

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd3c91ef43a4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('city', sa.String(length=120), nullable=False),
    sa.Column('state', sa.String(length=120), nullable=False),
    sa.Column('phone', sa.String(length=120), nullable=False),
    sa.Column('genres', sa.String(length=120), nullable=False),
    sa.Column('image_link', sa.String(length=500), nullable=False),
    sa.Column('facebook_link', sa.String(length=120), nullable=False),
    sa.Column('website', sa.String(length=120), nullable=False),
    sa.Column('seeking_venue', sa.Boolean(), nullable=False),
    sa.Column('seeking_description', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('venues',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('city', sa.String(length=120), nullable=False),
    sa.Column('state', sa.String(length=120), nullable=False),
    sa.Column('address', sa.String(length=120), nullable=False),
    sa.Column('phone', sa.String(length=120), nullable=False),
    sa.Column('genres', sa.String(length=120), nullable=False),
    sa.Column('image_link', sa.String(length=500), nullable=False),
    sa.Column('facebook_link', sa.String(length=120), nullable=False),
    sa.Column('website', sa.String(length=120), nullable=False),
    sa.Column('seeking_talent', sa.Boolean(), nullable=False),
    sa.Column('seeking_description', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('show',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=True),
    sa.Column('venue_name', sa.String(length=120), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.Column('artist_name', sa.String(length=120), nullable=False),
    sa.Column('artist_image_link', sa.String(length=500), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venues.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('show')
    op.drop_table('venues')
    op.drop_table('artists')
    # ### end Alembic commands ###
