from src.models_database.bookings import BookingsORM
from src.models_database.facilities import FacilitiesORM
from src.models_database.hotels import HotelsORM
from src.models_database.rooms import RoomsORM
from src.models_database.users import UsersORM
from src.schemas_API.bookings import BookingDTO
from src.schemas_API.facilities import FacilityReply
from src.schemas_API.hotels import Hotel
from src.schemas_API.users import User
from src.schemas_API.rooms import Room, RoomWithRels
from src.repositories.mappers.base import DataMapper

class HotelDataMapper(DataMapper):
    db_model = HotelsORM
    schema = Hotel

class BookingDataMapper(DataMapper):
    db_model = BookingsORM
    schema = BookingDTO

class UserDataMapper(DataMapper):
    db_model = UsersORM
    schema = User

class RoomDataMapper(DataMapper):
    db_model = RoomsORM
    schema = Room

class RoomDataWithRelsMapper(DataMapper):
    db_model = RoomsORM
    schema = RoomWithRels

class FacilityDataMapper(DataMapper):
    db_model = FacilitiesORM
    schema = FacilityReply