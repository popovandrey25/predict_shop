from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from core.models import Basket, BasketItem, Product, Order, OrderItem
from repositories.base import BaseRepository
from schemas.basket import BasketDetailResponse, BasketItemResponse


class BasketRepository(BaseRepository):
    model = Basket
    schema = BasketDetailResponse


    async def _get_basket(self, user_id):
        result = await self.session.execute(
            select(Basket).options(joinedload(Basket.items).joinedload(BasketItem.product)).filter_by(user_id=user_id)
        )
        basket = result.scalars().first()
        if not basket:
            basket = Basket(user_id=user_id)
            self.session.add(basket)
            await self.session.commit()
            await self.session.refresh(basket)
        return basket


    async def get_user_basket(self, user_id: int):
        basket = await self._get_basket(user_id)

        basket_items = [
            BasketItemResponse(
                id=item.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price
            )
            for item in basket.items
        ]
        return self.schema(id=basket.id, user_id=basket.user_id, items=basket_items)


    async def add_item_to_basket(self, user_id: int, product_id: int, quantity: int):
        basket = await self._get_basket(user_id)
        product = await self.session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        basket_item = next((item for item in basket.items if item.product_id == product_id), None)
        if basket_item:
            basket_item.quantity += quantity
        else:
            basket_item = BasketItem(
                basket_id=basket.id,
                product_id=product_id,
                quantity=quantity,
            )
            self.session.add(basket_item)

        await self.session.commit()
        await self.session.refresh(basket)

        basket_items = [
            BasketItemResponse(
                id=item.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price
            )
            for item in basket.items
        ]
        return self.schema(id=basket.id, user_id=basket.user_id, items=basket_items)


    async def update_item_quantity_in_basket(self, user_id: int, item_id: int, new_quantity: int):
        basket = await self._get_basket(user_id)
        basket_item = next((item for item in basket.items if item.id == item_id), None)

        if not basket_item:
            raise HTTPException(status_code=404, detail="Item not found in basket")

        basket_item.quantity = new_quantity

        await self.session.commit()
        await self.session.refresh(basket)

        basket_items = [
            BasketItemResponse(
                id=item.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price
            )
            for item in basket.items
        ]

        return self.schema(id=basket.id, user_id=basket.user_id, items=basket_items)


    async def remove_item_from_basket(self, user_id: int, item_id: int):
        basket = await self._get_basket(user_id)
        basket_item = next((item for item in basket.items if item.id == item_id), None)

        if not basket_item:
            raise HTTPException(status_code=404, detail="Item not found in basket")

        await self.session.delete(basket_item)

        await self.session.commit()
        await self.session.refresh(basket)

        basket_items = [
            BasketItemResponse(
                id=item.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price
            )
            for item in basket.items
        ]
        return self.schema(id=basket.id, user_id=basket.user_id, items=basket_items)


    async def _get_order(self, order_id):
        result = await self.session.execute(
            select(Order).options(joinedload(Order.order_items)).filter_by(id=order_id)
        )
        order = result.scalars().first()
        return order


    async def create_order(self, user_id: int):
        basket = await self._get_basket(user_id)

        if not basket.items:
            raise HTTPException(status_code=400, detail="Basket is empty")

        total_amount = sum(item.quantity * item.product.price for item in basket.items)

        order = Order(
            user_id=user_id,
            total_amount=total_amount,
            created_at=datetime.utcnow(),
            order_items=[
                OrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.product.price
                )
                for item in basket.items
            ]
        )
        self.session.add(order)

        await self.session.delete(basket)

        await self.session.commit()
        await self.session.refresh(order)

        order = await self._get_order(order_id=order.id)

        return {
            "id": order.id,
            "user_id": order.user_id,
            "total_amount": order.total_amount,
            "created_at": order.created_at,
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": item.price
                }
                for item in order.order_items
            ]
        }
