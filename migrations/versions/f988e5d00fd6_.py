"""empty message

Revision ID: f988e5d00fd6
Revises: 60e51a444165
Create Date: 2021-05-16 16:35:29.345895

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f988e5d00fd6'
down_revision = '60e51a444165'
branch_labels = None
depends_on = None


def upgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('business', 'approved')
    # ### end Alembic commands ###


def downgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.add_column('business', sa.Column('approved', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
