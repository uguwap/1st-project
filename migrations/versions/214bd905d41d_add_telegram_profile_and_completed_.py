"""Add telegram_profile and completed_request tables

Revision ID: 214bd905d41d
Revises: ce414d5e1ecc
Create Date: 2025-04-30 15:30:13.213277
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '214bd905d41d'
down_revision = 'ce414d5e1ecc'
branch_labels = None
depends_on = None


def upgrade():
    # Преобразуем строковые значения в логические
    op.execute("UPDATE request SET status = 'false' WHERE status = 'В работе'")
    op.execute("UPDATE request SET status = 'true' WHERE status = 'Завершено'")

    # Меняем тип поля status
    op.execute("ALTER TABLE request ALTER COLUMN status TYPE BOOLEAN USING status::BOOLEAN")

    # Создаём таблицу telegram_profile
    op.create_table(
        'telegram_profile',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('chat_id', sa.BigInteger(), nullable=False),
        sa.Column('username', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # Создаём таблицу completed_request
    op.create_table(
        'completed_request',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('city', sa.String(), nullable=False),
        sa.Column('processed_at', sa.DateTime(), nullable=False),
        sa.Column('client_phone', sa.String(), nullable=False),
        sa.Column('insect_type', sa.String(), nullable=False),
        sa.Column('treatment', sa.String(), nullable=False),
        sa.Column('source', sa.String(), nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('comment', sa.String(), nullable=True),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )


def downgrade():
    op.drop_table('completed_request')
    op.drop_table('telegram_profile')
    op.execute("ALTER TABLE request ALTER COLUMN status TYPE VARCHAR USING status::VARCHAR")