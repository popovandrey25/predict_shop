from pydantic import BaseModel, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str


class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr


class UserWithHashedPassword(UserResponse):
    hashed_password: str
