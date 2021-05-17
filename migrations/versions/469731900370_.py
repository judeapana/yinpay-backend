"""empty message

Revision ID: 469731900370
Revises: fb25a18bbba0
Create Date: 2021-05-17 09:26:36.424852

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '469731900370'
down_revision = 'fb25a18bbba0'
branch_labels = None
depends_on = None


def upgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###
