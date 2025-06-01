from src.schemas_API.facilities import FacilityReply, FacilityRequest
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilityService(BaseService):

    async def get_all_facilities(self) -> list[FacilityReply]:
        return await self.db.facilities.get_all()

    async def add_facility(self, facility_data: FacilityRequest) -> FacilityReply:
        facility = await self.db.facilities.add(facility_data)
        await self.db.commit()

        test_task.delay() # type: ignore
        return facility