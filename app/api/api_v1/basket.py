from fastapi import APIRouter

from api.api_v1.dependencies import UserIdDep, DBDep
from core.config import settings
from schemas.basket import BasketDetailResponse

router = APIRouter(
    prefix=settings.api.v1.basket,
    tags=["Продуктовая корзина"]
)

@router.get("", response_model=BasketDetailResponse)
async def get_basket(
    user_id: UserIdDep,
    db: DBDep
):
    basket = await db.baskets.get_user_basket(user_id)
    return basket
