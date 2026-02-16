from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.services.matching_engine import MatchingEngine
from app.models.ride_request import RideRequest
from app.models.cab import Cab
from app.models.ride import Ride
from app.models.passenger import Passenger
from app.schemas.ride import RideRequestCreate

router = APIRouter()
engine = MatchingEngine()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/ride/request")
async def create_ride(request: RideRequestCreate, db: AsyncSession = Depends(get_db)):

    async with db.begin():
        passenger = await db.get(Passenger, request.passenger_id)
        if not passenger:
            return {"error": "Passenger not found"}

        ride_request = RideRequest(**request.dict())
        db.add(ride_request)
        await db.flush()

        luggage = passenger.luggage_units

        # Try to find existing ride to join
        existing_ride = await engine.find_ride_to_join(db, ride_request, luggage)
        if existing_ride:
            ride_request.ride_id = existing_ride.id
            ride_request.status = "ASSIGNED"
            cab = await db.get(Cab, existing_ride.cab_id)
            cab.available_seats -= 1
            cab.available_luggage -= luggage
        else:
            # Create new ride
            cab = await engine.match_cab(db, ride_request)
            if cab:
                ride = Ride(cab_id=cab.id)
                db.add(ride)
                await db.flush()
                ride_request.ride_id = ride.id
                ride_request.status = "ASSIGNED"
                cab.available_seats -= 1
                cab.available_luggage -= luggage

        await db.commit()
        return {"message": "Ride Assigned"}

@router.post("/ride/cancel")
async def cancel_ride(request: dict, db: AsyncSession = Depends(get_db)):
    ride_request_id = request.get("ride_request_id")
    ride_request = await db.get(RideRequest, ride_request_id)
    if not ride_request or ride_request.status != "ASSIGNED":
        return {"message": "Cannot cancel"}

    ride = await db.get(Ride, ride_request.ride_id)
    cab = await db.get(Cab, ride.cab_id)
    passenger = await db.get(Passenger, ride_request.passenger_id)

    cab.available_seats += 1
    cab.available_luggage += passenger.luggage_units
    ride_request.status = "CANCELLED"

    # Check if ride has any assigned passengers left
    assigned = [r for r in ride.passengers if r.status == "ASSIGNED"]
    if not assigned:
        ride.status = "CANCELLED"

    await db.commit()
    return {"message": "Ride Cancelled"}
