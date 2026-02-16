from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.services.matching_engine import MatchingEngine
from app.models.ride_request import RideRequest
from app.models.cab import Cab
from app.schemas.ride import RideRequestCreate

router = APIRouter()
engine = MatchingEngine()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/ride/request")
async def create_ride(request: RideRequestCreate, db: AsyncSession = Depends(get_db)):

    async with db.begin():
        ride_request = RideRequest(**request.dict())
        db.add(ride_request)
        await db.flush()

        cab = await engine.match(db, ride_request)

        if cab:
            cab.available_seats -= 1
            cab.available_luggage -= 1

        return {"message": "Ride Assigned"}
