from datetime import date

from src.schemas_API.bookings import BookingAddDTO


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAddDTO(
        user_id=user_id,
        room_id=room_id,
        date_from=date.fromisoformat("2025-03-12"),
        date_to=date.fromisoformat("2025-03-16"),
        price=100,
    )
    new_booking = await db.bookings.add(booking_data)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.room_id == new_booking.room_id
    assert booking.user_id == new_booking.user_id
    # а еще можно вот так разом сравнить все параметры
    assert booking.model_dump(exclude={"id"}) == booking_data.model_dump()

    # обновить бронь
    updated_booking_data = BookingAddDTO(
        user_id=user_id,
        room_id=room_id,
        date_from=date.fromisoformat("2025-03-20"),
        date_to=date.fromisoformat("2025-03-25"),
        price=50,
    )
    await db.bookings.edit(updated_booking_data, id=new_booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.id == new_booking.id

    # удалить бронь
    await db.bookings.delete(id=new_booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not booking
