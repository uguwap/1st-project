"""update logic

Revision ID: 52cdf80a8164
Revises: e1ea2fa6c80a
Create Date: 2025-04-29 18:45:03.860975
"""

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision = '52cdf80a8164'
down_revision = 'e1ea2fa6c80a'
branch_labels = None
depends_on = None


def upgrade():
    # Удаляем таблицу client
    op.drop_table('client')

    # Обновляем таблицу reminder
    op.add_column('reminder', sa.Column('remind_at', sa.DateTime(), nullable=False))
    op.add_column('reminder', sa.Column('is_sent', sa.Boolean(), nullable=False))
    op.add_column('reminder', sa.Column('created_at', sa.DateTime(), nullable=False, server_default=text('NOW()')))
    op.drop_column('reminder', 'contact_date')
    op.drop_column('reminder', 'status')

    # Обновляем таблицу request
    op.add_column('request', sa.Column('client_phone', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.add_column('request', sa.Column('comment', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column('request', sa.Column('price', sa.Integer(), nullable=False))
    op.drop_column('request', 'final_price')
    op.drop_column('request', 'client_price')
    op.drop_column('request', 'title')
    op.drop_column('request', 'phone')
    op.drop_column('request', 'description')

    # Обновляем таблицу user
    op.add_column('user', sa.Column('created_at', sa.DateTime(), nullable=False, server_default=text('NOW()')))

    # Заполняем пустые телефоны заглушкой, иначе нельзя поставить NOT NULL
    op.execute("UPDATE \"user\" SET phone = '89999999999' WHERE phone IS NULL;")

    # Теперь можно поставить phone как NOT NULL
    op.alter_column('user', 'phone',
               existing_type=sa.VARCHAR(),
               nullable=False)

    op.drop_column('user', 'is_admin')
    op.drop_column('user', 'full_name')


def downgrade():
    # Восстановление таблицы user
    op.add_column('user', sa.Column('full_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('is_admin', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.alter_column('user', 'phone',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('user', 'created_at')

    # Восстановление таблицы request
    op.add_column('request', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('request', sa.Column('phone', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('request', sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('request', sa.Column('client_price', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.add_column('request', sa.Column('final_price', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.drop_column('request', 'price')
    op.drop_column('request', 'comment')
    op.drop_column('request', 'client_phone')

    # Восстановление таблицы reminder
    op.add_column('reminder', sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('reminder', sa.Column('contact_date', sa.DATE(), autoincrement=False, nullable=False))
    op.drop_column('reminder', 'created_at')
    op.drop_column('reminder', 'is_sent')
    op.drop_column('reminder', 'remind_at')

    # Восстановление таблицы client
    op.create_table(
        'client',
        sa.Column('phone', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('source', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.Column('verification_code', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column('verified', sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint('id', name='client_pkey')
    )
