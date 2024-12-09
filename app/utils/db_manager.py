from repositories.basket import BasketRepository
from repositories.order import OrderRepository
from repositories.product import ProductRepository
from repositories.user import UserRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UserRepository(self.session)
        self.products = ProductRepository(self.session)
        self.baskets = BasketRepository(self.session)
        self.orders = OrderRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
