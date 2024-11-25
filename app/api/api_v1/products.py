from typing import List

from fastapi import APIRouter, HTTPException

from api.api_v1.dependencies import DBDep, PaginationDep
from core.config import settings
from schemas.product import ProductResponse, ProductRequestAdd, ProductDetailResponse, ProductUpdate

router = APIRouter(
    prefix=settings.api.v1.products,
    tags=['Продукты']
)

@router.post("", response_model=ProductResponse)
async def create_product(
    product: ProductRequestAdd,
    db: DBDep,
):
    product = await db.products.add(product)
    await db.session.commit()
    return product


@router.get("/{product_id}", response_model=ProductDetailResponse)
async def get_product(
    product_id: int,
    db: DBDep,
):
    product = await db.products.get_one_or_none(id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product



@router.get("", response_model=List[ProductResponse])
async def list_products(
    pagination: PaginationDep,
    db: DBDep,
):
    return await db.products.get_all(
        limit=pagination.per_page, offset=pagination.per_page * (pagination.page - 1)
    )


@router.patch("/{product_id}", response_model=ProductDetailResponse)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: DBDep,
):
    await db.products.edit(product_update, exclude_unset=True, id=product_id)
    await db.commit()
    product = await db.products.get_one_or_none(id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
