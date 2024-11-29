from pydantic import BaseModel
from typing import List

class BasketItemBase(BaseModel):
    product_id: int
    quantity: int

class BasketItemCreate(BasketItemBase):
    pass

class BasketItemResponse(BasketItemBase):
    id: int
    price: float


class BasketDetailResponse(BaseModel):
    id: int
    user_id: int
    items: List[BasketItemResponse] = []
