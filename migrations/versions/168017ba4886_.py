"""empty message

Revision ID: 168017ba4886
Revises: f0249b5cd883
Create Date: 2021-07-07 08:53:18.112788

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '168017ba4886'
down_revision = 'f0249b5cd883'
branch_labels = None
depends_on = None


def upgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_attendance', sa.Column('attype', sa.Enum('Absent', 'Excused Duty', 'Present'), nullable=False))
    # ### end Alembic commands ###


def downgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_attendance', 'attype')
    # ### end Alembic commands ###