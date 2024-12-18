"""add user model

Revision ID: b1689eb2150b
Revises: 1b77ad88f2f2
Create Date: 2024-11-22 15:17:54.050324

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b1689eb2150b"
down_revision: Union[str, None] = "1b77ad88f2f2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
    )


def downgrade() -> None:
    op.drop_table("users")
