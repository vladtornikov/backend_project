from src.schemas_API.hotels import HotelADD


async def test_add_hotel(db):
    hotel_data = HotelADD(title="Hotel 5 stars", location="Сочи")
    await db.hotels.add(hotel_data)
    await db.commit()
