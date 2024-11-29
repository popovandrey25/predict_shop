from sqlalchemy import select
from sqlalchemy.orm import joinedload

from core.models import Basket
from repositories.base import BaseRepository
from schemas.basket import BasketDetailResponse


class BasketRepository(BaseRepository):
    model = Basket
    schema = BasketDetailResponse


    async def get_user_basket(self, user_id: int):
        result = await self.session.execute(
            select(Basket).options(joinedload(Basket.items)).filter_by(user_id=user_id)
        )
        basket = result.scalars().first()
        if not basket:
            basket = Basket(user_id=user_id)
            self.session.add(basket)
            await self.session.commit()
            await self.session.refresh(basket)
        return self.schema.model_validate(basket, from_attributes=True)
