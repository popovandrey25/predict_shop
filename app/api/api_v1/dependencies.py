from typing import Annotated
from fastapi import Depends

from utils.db_manager import DBManager
from core.models import db_helper


async def get_db():
    async with DBManager(session_factory=db_helper.session_factory) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
