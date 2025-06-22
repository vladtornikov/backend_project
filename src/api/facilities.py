from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache


from src.schemas_API.facilities import FacilityRequest
from src.api.dependencies import DBDep
from src.services.facilities import FacilityService


router = APIRouter(prefix="/facilities", tags=["Удобства в номерах"])


@router.get("", summary="Получаем все имеюищиеся удобства")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await FacilityService(db).get_all_facilities()


@router.post("", summary="Добавляем новое удобство")
async def add_facility(db: DBDep, facility_data: FacilityRequest = Body()):
    new_facility = await FacilityService(db).add_facility(facility_data)
    return {"status": "OK", "data": new_facility}
