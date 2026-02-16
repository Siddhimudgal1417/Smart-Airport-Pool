from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.database import get_db, engine, Base
from app.services.matching_engine import MatchingEngine
from app.models.ride_request import RideRequest
from app.models.cab import Cab
from app.models.ride import Ride
from app.models.passenger import Passenger

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class RideRequestInput(BaseModel):
    passenger_id: int
    pickup_lat: float
    pickup_lng: float
    drop_lat: float
    drop_lng: float
    detour_tolerance_percent: float

@app.on_event("startup")
async def startup():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Seed dummy data if none exist
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Cab))
        if not result.scalars().first():
            cabs = [
                Cab(driver_name="John Doe", license_plate="CAB-001", capacity=4, available_seats=4, available_luggage=4, current_lat=51.5074, current_lng=-0.1278),
                Cab(driver_name="Jane Smith", license_plate="CAB-002", capacity=4, available_seats=4, available_luggage=4, current_lat=51.5074, current_lng=-0.1278)
            ]
            session.add_all(cabs)
            
        # Seed a dummy passenger for the frontend demo
        result_p = await session.execute(select(Passenger).where(Passenger.id == 1))
        if not result_p.scalars().first():
            session.add(Passenger(id=1, name="Demo User", luggage_units=1, status="IDLE"))
            
        await session.commit()

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ride/request")
async def request_ride(input_data: RideRequestInput, db: AsyncSession = Depends(get_db)):
    # 1. Save the request
    new_req = RideRequest(**input_data.dict())
    db.add(new_req)
    await db.commit()
    await db.refresh(new_req)

    matcher = MatchingEngine()
    
    # 2. Try to join existing ride
    existing_ride = await matcher.find_ride_to_join(db, new_req, luggage=1)
    
    # Helper to update passenger
    passenger = await db.get(Passenger, input_data.passenger_id)
    if not passenger:
        passenger = Passenger(id=input_data.passenger_id, name="New User", luggage_units=1)
        db.add(passenger)

    if existing_ride:
        passenger.ride_id = existing_ride.id
        passenger.request_id = new_req.id
        passenger.status = "ASSIGNED"
        
        cab = await db.get(Cab, existing_ride.cab_id)
        cab.available_seats -= 1
        await db.commit()
        return {"success": True, "message": f"Joined shared ride with cab {cab.license_plate}"}

    # 3. Find new cab
    cab = await matcher.match_cab(db, new_req)
    if cab:
        new_ride = Ride(cab_id=cab.id)
        db.add(new_ride)
        await db.commit()
        await db.refresh(new_ride)
        
        passenger.ride_id = new_ride.id
        passenger.request_id = new_req.id
        passenger.status = "ASSIGNED"
        
        cab.available_seats -= 1
        await db.commit()
        return {"success": True, "message": f"Booked new cab {cab.license_plate}"}

    raise HTTPException(status_code=404, detail="No cabs available matching your criteria")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)