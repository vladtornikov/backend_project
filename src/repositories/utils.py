from datetime import date
from sqlalchemy import select, func

from src.models_database.bookings import BookingsORM
from src.models_database.rooms import RoomsORM


def rooms_ids_for_booking(
    date_from: date, date_to: date, hotel_id: int | None = None
) -> list[int]:
    booked_rooms_count = (
        select(BookingsORM.room_id, func.count("*").label("rooms_booked"))
        .select_from(BookingsORM)
        .filter(BookingsORM.date_from <= date_to, BookingsORM.date_to >= date_from)
        .group_by(BookingsORM.room_id)
        .cte(name="booked_rooms_count")
    )

    rooms_left = (
        select(
            RoomsORM.id.label("room_id"),
            (
                RoomsORM.quantity - func.coalesce(booked_rooms_count.c.rooms_booked, 0)
            ).label("rooms_available"),
        )
        .select_from(RoomsORM)
        .outerjoin(booked_rooms_count, RoomsORM.id == booked_rooms_count.c.room_id)
        .cte(name="rooms_left")
    )

    rooms_ids_for_hotel = select(RoomsORM.id).select_from(RoomsORM)
    if hotel_id is not None:
        rooms_ids_for_hotel = rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)

    rooms_ids_for_hotel = rooms_ids_for_hotel.subquery(name="rooms_ids_for_hotel")

    rooms_ids_to_get = select(rooms_left.c.room_id).filter(
        rooms_left.c.rooms_available > 0, rooms_left.c.room_id.in_(rooms_ids_for_hotel)
    )

    print(rooms_ids_to_get.compile(compile_kwargs={"literal_binds": True}))
    return rooms_ids_to_get
