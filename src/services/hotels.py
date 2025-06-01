from datetime import date

from src.api.dependencies import PaginationDep
from src.exceptions import check_dates, ObjectNotFoundException, HotelNotFoundException
from src.schemas_API.hotels import Hotel, HotelADD, HotelPatch
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_hotels(
            self,
            pagination: PaginationDep,
            title: str | None,
            location: str | None,
            date_from: date,
            date_to: date,
    ) -> list[Hotel]:

        check_dates(date_from, date_to)
        return await self.db.hotels.get_filtered_by_time(
            title=title,
            location=location,
            date_from=date_from,
            date_to=date_to,
            limit=pagination.per_page,
            offset=(pagination.page - 1) * pagination.per_page
        )

    async def get_hotel(self, hotel_id: int) -> Hotel:
        return await self.db.hotels.get_one(id=hotel_id)

    async def delete_hotel(self, hotel_id: int):
        await self.get_hotel_with_check(hotel_id)
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def add_hotel(self, hotel_data: HotelADD) -> Hotel:
        hotel: Hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def edit_hotel(self, hotel_data: HotelADD, hotel_id: int) -> None:
        try:
            await self.db.hotels.edit(hotel_data, id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        await self.db.commit()

    async def edit_hotel_partially(self, hotel_data: HotelPatch, hotel_id: int, exclude_unset: bool = False) -> None:
        try:
            await self.db.hotels.edit(hotel_data, exclude_unset=exclude_unset, id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        await self.db.commit()

    async def get_hotel_with_check(self, hotel_id: int) -> Hotel:
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex