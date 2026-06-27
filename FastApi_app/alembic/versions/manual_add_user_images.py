"""add user images and comment images

Revision ID: manual_add_user_images
Revises: e67c037fd66f
Create Date: 2026-06-26 16:40:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "manual_add_user_images"
down_revision: Union[str, None] = "e67c037fd66f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создаём таблицу для фото профиля пользователя
    op.create_table(
        "user_image",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_user_image_id", "user_image", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_user_image_id", table_name="user_image")
    op.drop_table("user_image")
