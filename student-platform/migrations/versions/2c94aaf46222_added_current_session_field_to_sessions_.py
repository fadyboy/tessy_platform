"""Added current_session field to Sessions table

Revision ID: 2c94aaf46222
Revises: 91b7193a1f8c
Create Date: 2020-03-10 21:48:30.997145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c94aaf46222'
down_revision = '91b7193a1f8c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sessions') as sessions_op:
        sessions_op.add_column(sa.Column('current_session', sa.Boolean(),  nullable=True))
        sessions_op.create_index(sessions_op.f('ix_sessions_current_session'), ['current_session'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sessions', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_sessions_current_session'))
        batch_op.drop_column('current_session')

    # ### end Alembic commands ###