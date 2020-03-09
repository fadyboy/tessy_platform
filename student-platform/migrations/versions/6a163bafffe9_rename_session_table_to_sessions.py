"""Rename Session table to Sessions

Revision ID: 6a163bafffe9
Revises: 18dad1a9529f
Create Date: 2020-02-20 22:20:17.177846

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a163bafffe9'
down_revision = '18dad1a9529f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('session', sa.String(length=16), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('sessions', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_sessions_session'), ['session'], unique=True)

    with op.batch_alter_table('session', schema=None) as batch_op:
        batch_op.drop_index('ix_session_session')

    op.drop_table('session')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('session',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('session', sa.VARCHAR(length=16), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('session', schema=None) as batch_op:
        batch_op.create_index('ix_session_session', ['session'], unique=1)

    with op.batch_alter_table('sessions', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_sessions_session'))

    op.drop_table('sessions')
    # ### end Alembic commands ###