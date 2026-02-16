import asyncio
from app.db.session import AsyncSessionLocal
from app.models.passenger import Passenger
from app.models.cab import Cab

async def create_sample_data():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # Create passenger
            passenger = Passenger(id=1, name="Demo User", luggage_units=1)
            session.add(passenger)

            # Create cabs
            cab1 = Cab(seat_capacity=4, available_seats=4, luggage_capacity=4, available_luggage=4, status="ACTIVE")
            cab2 = Cab(seat_capacity=4, available_seats=4, luggage_capacity=4, available_luggage=4, status="ACTIVE")
            session.add(cab1)
            session.add(cab2)

            await session.commit()

if __name__ == "__main__":
    asyncio.run(create_sample_data())
    print("Sample data created")