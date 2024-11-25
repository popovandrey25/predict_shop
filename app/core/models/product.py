from sqlalchemy import String, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base


class Product(Base):
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(String(200), nullable=True)
    price: Mapped[float] = mapped_column(Numeric(precision=10, scale=2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0)
