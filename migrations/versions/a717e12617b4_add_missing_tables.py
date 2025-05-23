"""add missing tables

Revision ID: a717e12617b4
Revises: aeb15afd1d94
Create Date: 2025-05-01 01:36:57.028317

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a717e12617b4'
down_revision = 'aeb15afd1d94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('completedrequest',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('original_request_id', sa.Uuid(), nullable=False),
    sa.Column('city', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('processed_at', sa.DateTime(), nullable=False),
    sa.Column('client_phone', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('insect_type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('treatment', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('source', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('address', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('comment', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('telegram_profile',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('telegram_profile')
    op.drop_table('completedrequest')
    # ### end Alembic commands ###
