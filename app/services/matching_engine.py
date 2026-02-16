from sqlalchemy import select
from app.models.cab import Cab
from app.utils.distance import haversine

class MatchingEngine:

    async def match(self, session, ride_request):
        result = await session.execute(
            select(Cab).where(
                Cab.available_seats > 0,
                Cab.status == "ACTIVE"
            ).with_for_update()
        )

        cabs = result.scalars().all()

        best_cab = None
        min_cost = float("inf")

        for cab in cabs:
            if cab.available_luggage < 1:
                continue

            cost = self.calculate_cost(cab, ride_request)

            if cost < min_cost:
                min_cost = cost
                best_cab = cab

        return best_cab

    def calculate_cost(self, cab, ride_request):
        return haversine(
            ride_request.pickup_lat,
            ride_request.pickup_lng,
            ride_request.drop_lat,
            ride_request.drop_lng
        )
