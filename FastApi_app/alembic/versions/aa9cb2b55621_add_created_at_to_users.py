"""add_created_at_to_users

Revision ID: aa9cb2b55621
Revises: manual_add_user_images
Create Date: 2026-06-26 22:52:31.025074

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "aa9cb2b55621"
down_revision: Union[str, Sequence[str], None] = "manual_add_user_images"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Проверяем существование колонки и добавляем если её нет
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col["name"] for col in inspector.get_columns("users")]

    if "created_at" not in columns:
        op.add_column(
            "users",
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=True,
            ),
        )
        # Обновляем существующие записи
        op.execute("UPDATE users SET created_at = NOW() WHERE created_at IS NULL")


def downgrade() -> None:
    # Удаляем колонку created_at
    op.drop_column("users", "created_at")
