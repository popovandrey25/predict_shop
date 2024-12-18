from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import mapped_column, relationship, Mapped

from core.models import Base, Product


class Basket(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True)
    items: Mapped[list["BasketItem"]] = relationship(
        "BasketItem",
        back_populates="basket",
        cascade="all, delete-orphan",
        lazy="joined"
    )

class BasketItem(Base):
    basket_id: Mapped[int] = mapped_column(ForeignKey("baskets.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    basket: Mapped[Basket] = relationship("Basket", back_populates="items")
    product: Mapped[Product] = relationship("Product", back_populates="basket_items")
