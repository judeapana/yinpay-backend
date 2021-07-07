"""empty message

Revision ID: a7b4b05dc669
Revises: 382682ec7a1f
Create Date: 2021-05-28 15:06:55.651834

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a7b4b05dc669'
down_revision = '382682ec7a1f'
branch_labels = None
depends_on = None


def upgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'tax', 'period', ['period_id'], ['id'], ondelete='cascade')
    op.add_column('user_attendance', sa.Column('time', sa.DateTime(), nullable=False))
    op.add_column('user_attendance', sa.Column('type', sa.Enum('Clock In', 'Clock Out'), nullable=True))
    op.drop_column('user_attendance', 'clock_out_date')
    op.drop_column('user_attendance', 'clock_in_date')
    # ### end Alembic commands ###


def downgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_attendance', sa.Column('clock_in_date', mysql.DATETIME(), nullable=False))
    op.add_column('user_attendance', sa.Column('clock_out_date', mysql.DATETIME(), nullable=False))
    op.drop_column('user_attendance', 'type')
    op.drop_column('user_attendance', 'time')
    op.drop_constraint(None, 'tax', type_='foreignkey')
    # ### end Alembic commands ###