from fastapi import APIRouter

from api.api_v1.dependencies import UserIdDep, DBDep
from core.config import settings

router = APIRouter(
    prefix=settings.api.v1.orders,
    tags=["Заказы"],
)


@router.post("")
async def create_order(
    user_id: UserIdDep,
    db: DBDep
):
    return await db.baskets.create_order(user_id)


@router.get("")
async def get_orders(
    user_id: UserIdDep,
    db: DBDep
):
    return await db.orders.get_all_orders(user_id)
