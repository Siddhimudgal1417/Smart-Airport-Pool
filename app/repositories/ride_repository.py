from app.models.ride import Ride

class RideRepository:

    async def create_ride(self, session, cab_id):
        ride = Ride(cab_id=cab_id)
        session.add(ride)
        await session.flush()
        return ride
