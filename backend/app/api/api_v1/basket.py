from fastapi import APIRouter

from api.api_v1.dependencies import UserIdDep, DBDep
from core.config import settings
from schemas.basket import BasketDetailResponse, BasketItemCreate

router = APIRouter(
    prefix=settings.api.v1.basket,
    tags=["Продуктовая корзина"]
)

@router.get("", response_model=BasketDetailResponse)
async def get_basket(
    user_id: UserIdDep,
    db: DBDep
):
    return await db.baskets.get_user_basket(user_id)


@router.post("/add", response_model=BasketDetailResponse)
async def add_to_basket(
    item: BasketItemCreate,
    db: DBDep,
    user_id: UserIdDep,
):
    return await db.baskets.add_item_to_basket(user_id, item.product_id, item.quantity)


@router.post("/{item_id}")
async def update_item_in_basket(
    item_id: int,
    db: DBDep,
    user_id: UserIdDep,
    quantity: int
):
    return await db.baskets.update_item_quantity_in_basket(user_id, item_id, quantity)


@router.delete("/{item_id}", response_model=BasketDetailResponse)
async def delete_item_from_basket(
    item_id: int,
    db: DBDep,
    user_id: UserIdDep,
):
    return await db.baskets.remove_item_from_basket(user_id, item_id)
