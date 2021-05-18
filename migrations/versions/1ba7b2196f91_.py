"""empty message

Revision ID: 1ba7b2196f91
Revises: d9a1be78d481
Create Date: 2021-05-18 23:25:19.612154

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ba7b2196f91'
down_revision = 'd9a1be78d481'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('venue_image_link', sa.String(length=500), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shows', 'venue_image_link')
    # ### end Alembic commands ###
