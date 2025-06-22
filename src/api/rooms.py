from fastapi import APIRouter, Body, Query
from datetime import date

from src.exceptions import (
    RoomNotFoundException,
    RoomNotFoundHTTPException,
    HotelNotFoundHTTPException,
    HotelNotFoundException,
)
from src.schemas_API.rooms import RoomAddRequest, RoomPatchRequest
from src.api.dependencies import DBDep
from src.services.rooms import RoomsService

router = APIRouter(prefix="/hotels", tags=["Номера в отелях"])


@router.get("/{hotel_id}/rooms", summary="Получение всех комнат в определенном отеле")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    return await RoomsService(db).get_all_rooms_in_hotel(hotel_id, date_from, date_to)


@router.get(
    "/{hotel_id}/rooms/{room_id}", summary="Получение данных определенной комнаты"
)
async def get_data_about_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        return await RoomsService(db).get_one_room(room_id, hotel_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.delete("/{hotels_id}/rooms/{room_id}", summary="Удаляем комнату из базы данных")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        await RoomsService(db).delete_room(hotel_id, room_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "OK"}


@router.post(
    "/{hotel_id}/rooms",
    summary="Добавляем новые комнаты в определенный отель",
)
async def create_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest = Body):
    try:
        room = await RoomsService(db).add_room(room_data, hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "data": room}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Полное обновление данных о комнате",
    description="Нужно обязательно ввести все параметры",
)
async def update_room(
    db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest = Body
):
    try:
        await RoomsService(db).edit_room(hotel_id, room_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление данных о комнате",
    description="Необязательно передавать все параметры",
)
async def partially_edit_room(
    db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest
):
    try:
        await RoomsService(db).edit_room_partially(hotel_id, room_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "OK"}
