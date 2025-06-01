from src.repositories.hotels import HotelRepository
from src.repositories.rooms import RoomsRepository
from src.repositories.users import UsersRepository
from src.repositories.bookings import BookingsRepository
from src.repositories.facility import FacilitiesRepository, RoomsFacilitiesRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.hotels = HotelRepository(self.session)
        self.rooms = RoomsRepository(self.session)
        self.users = UsersRepository(self.session)
        self.bookings = BookingsRepository(self.session)
        self.facilities = FacilitiesRepository(self.session)
        self.rooms_facilities = RoomsFacilitiesRepository(self.session)

        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
