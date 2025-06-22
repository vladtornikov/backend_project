# ruff: noqa: E402

from typing import Callable

import pytest
import json

from pydantic import BaseModel
from unittest import mock
from httpx import ASGITransport, AsyncClient

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from src.api.dependencies import get_db
from src.config import settings
from src.database import BaseORM, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models_database import *  # noqa
from src.schemas_API.hotels import HotelADD
from src.schemas_API.rooms import RoomAdd
from src.utils.database_cntxt_mngr import DBManager


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="function")
async def db(check_test_mode) -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


async def db_null_pool() -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


app.dependency_overrides[get_db] = db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(BaseORM.metadata.drop_all)
        await conn.run_sync(BaseORM.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def add_hotels_and_rooms(setup_database):
    with open("tests/mock_hotels.json", encoding="utf-8") as hotels:
        hotels_deserial: list[dict] = json.load(hotels)
    with open("tests/mock_rooms.json", encoding="utf-8") as rooms:
        rooms_deserial: list[dict] = json.load(rooms)

    hotels_pydantic: list[BaseModel] = [
        HotelADD.model_validate(hotel) for hotel in hotels_deserial
    ]
    rooms_pydantic: list[BaseModel] = [
        RoomAdd.model_validate(room) for room in rooms_deserial
    ]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels_pydantic)
        await db_.rooms.add_bulk(rooms_pydantic)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="function")
async def register_user(ac, setup_database):
    await ac.post(
        "/auth/register",
        json={"email": "kot@pes.com", "password": "jack123@rambler.ru"},
    )


@pytest.fixture(scope="function")
async def authenticated_ac(register_user: Callable, ac: AsyncClient) -> AsyncClient:
    await ac.post(
        "/auth/login", json={"email": "kot@pes.com", "password": "jack123@rambler.ru"}
    )
    assert "access_token" in ac.cookies
    yield ac
