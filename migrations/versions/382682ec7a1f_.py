"""empty message

Revision ID: 382682ec7a1f
Revises: 52d703767da6
Create Date: 2021-05-27 22:48:05.652887

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '382682ec7a1f'
down_revision = '52d703767da6'
branch_labels = None
depends_on = None


def upgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.execute("SET FOREIGN_KEY_CHECKS=0")
    op.create_foreign_key(None, 'attendance', 'period', ['period_id'], ['id'], ondelete='cascade')
    op.drop_index('period_id', table_name='social_security_rate')
    op.drop_index('period_id', table_name='tax')
    op.execute("SET FOREIGN_KEY_CHECKS=1")
    # ### end Alembic commands ###


def downgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.create_index('period_id', 'tax', ['period_id'], unique=True)
    op.create_index('period_id', 'social_security_rate', ['period_id'], unique=True)
    op.drop_constraint(None, 'attendance', type_='foreignkey')
    # ### end Alembic commands ###