from fastapi import APIRouter, Body, Query
from datetime import date

from fastapi_cache.decorator import cache

from src.exceptions import ObjectNotFoundException, HotelNotFoundHTTPException, HotelNotFoundException
from src.schemas_API.hotels import HotelADD, HotelPatch
from src.api.dependencies import PaginationDep, DBDep
from src.services.hotels import HotelService

router = APIRouter(prefix='/hotels', tags=['Отели'])

@router.get(
    '',
    summary='Тут мы получаем данные об отеле',
    description='Если ввести id, name или (и) title, то получим данные о конкретном отеле'
)
@cache(expire=20)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Адрес отеля"),
        date_from: date = Query(example="2025-02-10"),
        date_to: date = Query(example="2025-02-15")
):
    return await HotelService(db).get_hotels(
        pagination,
        title,
        location,
        date_from,
        date_to,
    )


@router.get(
    '/{hotel_id}',
    summary='Тут мы получаем один отель по его айди'
)
async def get_hotel(db: DBDep, hotel_id: int):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

@router.delete(
    "/{hotel_id}",
    summary='Тут мы удаляем отель'
)
async def delete_hotel(db: DBDep, hotel_id: int):
    try:
        await HotelService(db).delete_hotel(hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK"}

@router.post(
    '',
    summary='Тут мы можем добавить данные о новом отеле'
)
async def create_hotel(db: DBDep, hotel_data: HotelADD = Body(openapi_examples={
    "1": {
        "summary": "Бангкок",
        "value": {
            "title": "Отель Амара Бангкок",
            "location": "Бангкок, Суравонг, 10500",
        }
    },
    "2": {
        "summary": "Москва",
        "value": {
            "title": "Рэдиссон Славянская",
            "location": "Площадь трех вокзалов, 3",
        }
    }
})
):
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "OK", "data": hotel}

@router.put(
    "/{hotel_id}",
    summary='Обновление данных об отеле',
    description='Тут мы полностью обновляем данные об отеле: нужно обязательно передать и name, и title'
)
async def change_whole_hotel(db: DBDep, hotel_data: HotelADD, hotel_id: int):
    try:
        await HotelService(db).edit_hotel(hotel_data, hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK"}

@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Тут мы частично обновляем данные об отеле: можно отправить title, а можно location",
)
async def partially_change_hotel(db: DBDep, hotel_id:int, hotel_data: HotelPatch = Body):
    try:
        await HotelService(db).edit_hotel_partially(hotel_data, hotel_id, exclude_unset=True)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK"}


