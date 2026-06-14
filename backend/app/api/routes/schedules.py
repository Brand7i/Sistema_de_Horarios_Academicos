from fastapi import APIRouter

from backend.app.domain.sample_data import build_sample_request
from backend.app.domain.entities import ScheduleRequest, ScheduleResponse
from backend.app.services.schedule_service import ScheduleService


router = APIRouter(prefix="/schedules", tags=["schedules"])

service = ScheduleService()


@router.get("/sample", response_model=ScheduleResponse)
def generate_sample_schedule() -> ScheduleResponse:
    request = build_sample_request()
    return service.generate_schedule(request)


@router.post("/generate", response_model=ScheduleResponse)
def generate_schedule(request: ScheduleRequest) -> ScheduleResponse:
    return service.generate_schedule(request)
