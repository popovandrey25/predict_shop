from fastapi import APIRouter

from core.config import settings
from .auth import router as auth_router
from .products import router as product_router
from .basket import router as basket_router


router = APIRouter(
    prefix=settings.api.v1.prefix,
)
router.include_router(auth_router)
router.include_router(product_router)
router.include_router(basket_router)
