from typing import Annotated
from pydantic import BaseModel
from fastapi import Query, Depends, Request

from src.database import async_session_maker
from src.exceptions import (
    IncorrectTokenException,
    IncorrectTokenHTTPException,
    NoAccessTokenHTTPException,
)
from src.services.auth import AuthService
from src.utils.database_cntxt_mngr import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int, Query(default=1, ge=1)]
    per_page: Annotated[int | None, Query(6, ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise NoAccessTokenHTTPException
    return token


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]


def get_current_user_id(db: DBDep, token: str = Depends(get_token)) -> int:
    try:
        data_from_token = AuthService(db).decode_token(token)
    except IncorrectTokenException:
        raise IncorrectTokenHTTPException
    return data_from_token.get("user_id")


UserIdDep = Annotated[int, Depends(get_current_user_id)]
