from src.exceptions import check_dates, RoomNotFoundException
from src.schemas_API.bookings import BookingDTO, BookingAddDTO, BookingAddRequestDTO
from src.schemas_API.hotels import Hotel
from src.schemas_API.rooms import Room
from src.services.base import BaseService
from src.services.rooms import RoomsService


class BookingService(BaseService):
    async def get_all_bookings(self) -> list[BookingDTO]:
        return await self.db.bookings.get_all()

    async def get_booking_authorized_user(self, user_id: int) -> list[BookingDTO]:
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def add_booking(self, user_id: int, booking_data: BookingAddRequestDTO):
        check_dates(booking_data.date_from, booking_data.date_to)
        try:
            room: Room = await RoomsService(self.db).get_room_with_check(
                booking_data.room_id
            )
        except RoomNotFoundException as ex:
            raise ex
        hotel: Hotel = await self.db.hotels.get_one(id=room.hotel_id)
        room_price: int = room.price
        _booking_data = BookingAddDTO(
            user_id=user_id,
            price=room_price,
            **booking_data.dict(),
        )
        booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
        await self.db.commit()
        return booking
