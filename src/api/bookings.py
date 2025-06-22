from fastapi import APIRouter


from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import (
    AllRoomsAreBookedException,
    RoomNotFoundException,
    AllRoomsAreBookedHTTPException,
    RoomNotFoundHTTPException,
)
from src.schemas_API.bookings import BookingAddRequestDTO
from src.services.bookings import BookingService


router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("", summary="Добавляем новое бронирование")
async def booking(booking_data: BookingAddRequestDTO, db: DBDep, user_id: UserIdDep):
    try:
        booking = await BookingService(db).add_booking(user_id, booking_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
    return {"status": "OK", "data": booking}


@router.get("", summary="Получаем все бронирования")
async def get_all(db: DBDep):
    all_bookings = await BookingService(db).get_all_bookings()
    return {"status": "OK", "data": all_bookings}


@router.get("/me", summary="Получаем бронирование аутентифицированного пользователя")
async def get_a_booking(db: DBDep, user_id: UserIdDep):
    bookings = await BookingService(db).get_booking_authorized_user(user_id)
    return {"status": "OK", "data": bookings}
