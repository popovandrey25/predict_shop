"""add product model

Revision ID: c54d009baf0e
Revises: b1689eb2150b
Create Date: 2024-11-25 11:20:32.451906

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c54d009baf0e"
down_revision: Union[str, None] = "b1689eb2150b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=200), nullable=True),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("stock", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_products")),
        sa.UniqueConstraint("name", name=op.f("uq_products_name")),
    )


def downgrade() -> None:
    op.drop_table("products")
