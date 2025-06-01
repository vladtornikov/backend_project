from pydantic import BaseModel, Field


class HotelADD(BaseModel):
    title: str
    location: str

class Hotel(HotelADD):
    id: int

class HotelPatch(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)




