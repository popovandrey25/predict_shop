from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class ProductBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=200)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)


class ProductRequestAdd(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None


class ProductResponse(BaseModel):
    id: int
    name: str


class ProductDetailResponse(ProductResponse):
    description: Optional[str]
    price: float
    stock: int
