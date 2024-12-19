from repositories.base import BaseRepository
from core.models.product import Product
from schemas.product import ProductDetailResponse


class ProductRepository(BaseRepository):
    model = Product
    schema = ProductDetailResponse
