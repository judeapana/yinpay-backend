"""empty message

Revision ID: 7793dd9b2a69
Revises: 977751c9957f
Create Date: 2021-05-16 20:22:14.383404

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '7793dd9b2a69'
down_revision = '977751c9957f'
branch_labels = None
depends_on = None


def upgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_attendance', sa.Column('clock_in_date', sa.DateTime(), nullable=False))
    op.add_column('user_attendance', sa.Column('clock_out_date', sa.DateTime(), nullable=False))
    op.drop_column('user_attendance', 'date')
    # ### end Alembic commands ###


def downgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_attendance', sa.Column('date', sa.DATE(), nullable=False))
    op.drop_column('user_attendance', 'clock_out_date')
    op.drop_column('user_attendance', 'clock_in_date')
    # ### end Alembic commands ###
