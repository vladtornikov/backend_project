from datetime import date

from src.exceptions import ObjectNotFoundException, RoomNotFoundException, check_dates
from src.schemas_API.facilities import RoomsFacilitiesAdd
from src.schemas_API.rooms import (
    Room,
    RoomAdd,
    RoomPatch,
    RoomAddRequest,
    RoomPatchRequest,
)
from src.services.base import BaseService
from src.services.hotels import HotelService


class RoomsService(BaseService):
    async def get_all_rooms_in_hotel(
        self, hotel_id: int, date_from: date, date_to: date
    ) -> list[Room]:
        check_dates(date_from, date_to)
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_one_room(self, room_id: int, hotel_id: int) -> Room:
        room: Room = await self.db.rooms.get_room_with_facilities(
            id=room_id, hotel_id=hotel_id
        )
        await self.db.commit()
        return room

    async def delete_room(self, hotel_id: int, room_id: int):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)
        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()

    async def add_room(self, data: RoomAddRequest, hotel_id: int) -> Room:
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        _room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
        room: Room = await self.db.rooms.add(_room_data)

        if data.facilities_ids:
            rooms_facilities_data = [
                RoomsFacilitiesAdd(room_id=room.id, facility_id=f_id)
                for f_id in data.facilities_ids
            ]
            await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()
        return room

    async def edit_room(
        self, hotel_id: int, room_id: int, room_data: RoomAddRequest
    ) -> None:
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)
        _room_data = RoomAdd(**room_data.model_dump(), hotel_id=hotel_id)
        await self.db.rooms.edit(_room_data, id=room_id)
        await self.db.rooms_facilities.set_room_facilities(
            room_id, facilities_ids=room_data.facilities_ids
        )
        await self.db.commit()

    async def edit_room_partially(
        self,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
    ) -> None:
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)
        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
        await self.db.rooms.edit(
            _room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id
        )
        if "facilities_ids" in _room_data_dict:
            await self.db.rooms_facilities.set_room_facilities(
                room_id, facilities_ids=_room_data_dict["facilities_ids"]
            )
        await self.db.commit()

    async def get_room_with_check(self, room_id: int) -> Room:
        try:
            return await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
