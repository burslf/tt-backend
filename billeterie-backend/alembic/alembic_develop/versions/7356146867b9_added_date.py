"""added date

Revision ID: 7356146867b9
Revises: 97dc6e56839d
Create Date: 2022-11-20 01:26:44.405164

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7356146867b9'
down_revision = '97dc6e56839d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event_created', sa.Column('network_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'event_created', 'network', ['network_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'event_created', type_='foreignkey')
    op.drop_column('event_created', 'network_id')
    # ### end Alembic commands ###
