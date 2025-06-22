from datetime import date
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload
from typing import Any
from pydantic import BaseModel

from src.exceptions import RoomNotFoundException
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper, RoomDataWithRelsMapper
from src.repositories.utils import rooms_ids_for_booking
from src.models_database.rooms import RoomsORM


class RoomsRepository(BaseRepository):
    model = RoomsORM
    mapper = RoomDataMapper

    async def get_filtered_by_time(
        self, hotel_id: int, date_from: date, date_to: date
    ) -> list[BaseModel]:
        rooms_ids_to_get: list[int] = rooms_ids_for_booking(
            date_to, date_from, hotel_id
        )

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(self.model.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [
            RoomDataWithRelsMapper.map_to_domain_entity(model)
            for model in result.unique().scalars().all()
        ]

    async def get_room_with_facilities(self, **filter_by: Any) -> BaseModel:
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise RoomNotFoundException
        return RoomDataWithRelsMapper.map_to_domain_entity(model)
