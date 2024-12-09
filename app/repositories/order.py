from sqlalchemy import select
from sqlalchemy.orm import joinedload

from core.models import Order
from repositories.base import BaseRepository
from schemas.order import OrderDetailResponse


class OrderRepository(BaseRepository):
    model = Order
    schema = OrderDetailResponse

    async def get_all_orders(self, user_id):
        result = await self.session.execute(
            select(Order).options(joinedload(Order.order_items)).filter_by(user_id=user_id)
        )
        # return [self.schema.model_validate(model, from_attributes=True) for model in result.unique().scalars().all()]
        orders = result.unique().scalars().all()
        response = [
            {
                "id": order.id,
                "user_id": order.user_id,
                "total_amount": order.total_amount,
                "created_at": order.created_at.isoformat(),
                "items": [
                    {
                        "product_id": item.product_id,
                        "quantity": item.quantity,
                        "price": item.price
                    }
                    for item in order.order_items
                ]
            }
            for order in orders
        ]
        return response
