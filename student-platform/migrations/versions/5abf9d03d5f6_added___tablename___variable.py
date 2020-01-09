"""Added __tablename__ variable

Revision ID: 5abf9d03d5f6
Revises: f75a90605779
Create Date: 2020-01-06 22:21:56.169517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5abf9d03d5f6'
down_revision = 'f75a90605779'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('AdminUsers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('role', sa.String(length=16), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_AdminUsers_email'), 'AdminUsers', ['email'], unique=True)
    op.create_index(op.f('ix_AdminUsers_username'), 'AdminUsers', ['username'], unique=True)
    op.drop_index('ix_admin_users_email', table_name='admin_users')
    op.drop_index('ix_admin_users_username', table_name='admin_users')
    op.drop_table('admin_users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin_users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), nullable=True),
    sa.Column('email', sa.VARCHAR(length=128), nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=128), nullable=True),
    sa.Column('role', sa.VARCHAR(length=16), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_admin_users_username', 'admin_users', ['username'], unique=1)
    op.create_index('ix_admin_users_email', 'admin_users', ['email'], unique=1)
    op.drop_index(op.f('ix_AdminUsers_username'), table_name='AdminUsers')
    op.drop_index(op.f('ix_AdminUsers_email'), table_name='AdminUsers')
    op.drop_table('AdminUsers')
    # ### end Alembic commands ###