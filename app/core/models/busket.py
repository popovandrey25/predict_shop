from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship, Mapped

from core.models import Base


class Basket(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True)
    items: Mapped[list["BasketItem"]] = relationship(
        "BasketItem",
        back_populates="basket",
        cascade="all, delete-orphan",
    )

class BasketItem(Base):
    basket_id: Mapped[int] = mapped_column(ForeignKey("baskets.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    basket: Mapped[Basket] = relationship("Basket", back_populates="items")
