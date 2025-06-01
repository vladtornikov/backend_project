from sqlalchemy import select
from datetime import date

from src.models_database.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.repositories.mappers.mappers import HotelDataMapper
from src.models_database.hotels import HotelsORM
from src.schemas_API.hotels import Hotel


class HotelRepository(BaseRepository):
    model = HotelsORM
    mapper = HotelDataMapper

    async def get_filtered_by_time(
            self,
            title: str | None,
            location: str | None,
            date_from: date,
            date_to: date,
            limit: int,
            offset: int | None
    ) -> list[Hotel]:
        
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_get = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
            .cte('hotels_ids_get')
        )

        query = (
            select(self.model)
            .select_from(self.model)
            .filter(self.model.id.in_(hotels_ids_get))
        )
        if title:
            query = query.filter(self.model.title.ilike(f'%{title}%'))
        if location:
            query = query.filter(self.model.location.ilike(f'%{location}%'))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        print(query.compile(compile_kwargs={'literal_binds': True}))
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]
