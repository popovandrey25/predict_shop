"""add busket and busket_item model

Revision ID: 8a8a409ac402
Revises: c54d009baf0e
Create Date: 2024-11-28 13:12:12.177768

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8a8a409ac402"
down_revision: Union[str, None] = "c54d009baf0e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "baskets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_baskets_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_baskets")),
        sa.UniqueConstraint("user_id", name=op.f("uq_baskets_user_id")),
    )
    op.create_table(
        "basket_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("basket_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["basket_id"],
            ["baskets.id"],
            name=op.f("fk_basket_items_basket_id_baskets"),
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
            name=op.f("fk_basket_items_product_id_products"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_basket_items")),
    )


def downgrade() -> None:
    op.drop_table("basket_items")
    op.drop_table("baskets")
