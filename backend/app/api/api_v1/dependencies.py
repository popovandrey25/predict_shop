from typing import Annotated
from fastapi import Depends, HTTPException, Query
from pydantic import BaseModel
from starlette.requests import Request

from services.auth import AuthService
from utils.db_manager import DBManager
from core.models import db_helper


async def get_db():
    async with DBManager(session_factory=db_helper.session_factory) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Вы не предоставили токен доступа")
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(10, ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]
