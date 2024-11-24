from pydantic import EmailStr
from sqlalchemy import select

from repositories.base import BaseRepository
from core.models import User
from schemas.user import UserResponse, UserWithHashedPassword


class UserRepository(BaseRepository):
    model = User
    schema = UserResponse

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPassword.model_validate(
            model, from_attributes=True
        )
