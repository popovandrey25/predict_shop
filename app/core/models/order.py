from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base


class Order(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    total_amount: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    order_items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="order_items")
