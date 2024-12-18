from datetime import datetime
from typing import List

from pydantic import BaseModel


class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    price: float


class OrderDetailResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    created_at: datetime
    items: List[OrderItemResponse] = []
