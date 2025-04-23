"""user upgrade

Revision ID: 533941db5e14
Revises: f6298e858321
Create Date: 2025-04-23 21:38:07.359332

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel  # Необходим для совместимости с SQLModel

from sqlalchemy.dialects import postgresql
# revision identifiers, used by Alembic.



revision = '533941db5e14'
down_revision = 'f6298e858321'
branch_labels = None
depends_on = None


def upgrade():
    client_source_enum = sa.Enum('site', 'call', 'ad', 'referral', name='clientsource')
    client_source_enum.create(op.get_bind(), checkfirst=True)

    op.add_column('client', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.alter_column('client', 'phone', type_=sa.String())
    op.execute("ALTER TABLE client ALTER COLUMN source TYPE clientsource USING source::clientsource")


def downgrade():
    op.alter_column('client', 'source', type_=sa.String())
    op.alter_column('client', 'phone', type_=sa.Integer())
    op.drop_column('client', 'updated_at')
    client_source_enum = sa.Enum('site', 'call', 'ad', 'referral', name='clientsource')
    client_source_enum.drop(op.get_bind(), checkfirst=True)

