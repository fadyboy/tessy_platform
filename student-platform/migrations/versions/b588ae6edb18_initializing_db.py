"""Initializing db

Revision ID: b588ae6edb18
Revises: 
Create Date: 2020-01-11 19:52:04.922800

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b588ae6edb18'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('role', sa.String(length=16), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Users_email'), 'Users', ['email'], unique=True)
    op.create_index(op.f('ix_Users_username'), 'Users', ['username'], unique=True)
    op.create_table('classroom',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('classroom_name', sa.String(length=128), nullable=True),
    sa.Column('classroom_symbol', sa.String(length=8), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('staff',
    sa.Column('firstname', sa.String(length=64), nullable=False),
    sa.Column('middlename', sa.String(length=64), nullable=True),
    sa.Column('surname', sa.String(length=64), nullable=False),
    sa.Column('gender', sa.String(length=16), nullable=True),
    sa.Column('birthday', sa.DateTime(), nullable=True),
    sa.Column('contact_number', sa.String(length=128), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student',
    sa.Column('firstname', sa.String(length=64), nullable=False),
    sa.Column('middlename', sa.String(length=64), nullable=True),
    sa.Column('surname', sa.String(length=64), nullable=False),
    sa.Column('gender', sa.String(length=16), nullable=True),
    sa.Column('birthday', sa.DateTime(), nullable=True),
    sa.Column('contact_number', sa.String(length=128), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('parent_guardian_name', sa.String(length=128), nullable=True),
    sa.Column('classroom_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['classroom_id'], ['classroom.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('student')
    op.drop_table('staff')
    op.drop_table('classroom')
    op.drop_index(op.f('ix_Users_username'), table_name='Users')
    op.drop_index(op.f('ix_Users_email'), table_name='Users')
    op.drop_table('Users')
    # ### end Alembic commands ###