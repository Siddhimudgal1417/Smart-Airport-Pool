from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.cab import Cab
from app.models.ride import Ride
from app.models.ride_request import RideRequest
from app.models.passenger import Passenger
from app.utils.distance import haversine

class MatchingEngine:

    async def match_cab(self, session, ride_request):
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
            if cab.available_luggage < 1:  # assume luggage 1 for now
                continue

            cost = self.calculate_cost(cab, ride_request)

            if cost < min_cost:
                min_cost = cost
                best_cab = cab

        return best_cab

    def calculate_cost(self, cab, ride_request):
        return haversine(
            cab.current_lat,
            cab.current_lng,
            ride_request.pickup_lat,
            ride_request.pickup_lng
        )

    async def find_ride_to_join(self, session, new_request, luggage):
        # Get ongoing rides
        result = await session.execute(
            select(Ride)
            .where(Ride.status == "ONGOING")
            .options(selectinload(Ride.passengers).selectinload(Passenger.request))
        )
        rides = result.scalars().all()

        for ride in rides:
            cab = await session.get(Cab, ride.cab_id)
            if not cab or cab.available_seats <= 0 or cab.available_luggage < luggage:
                continue

            # Get current assigned passengers
            # Fix: Extract the 'request' object from the passenger, as Passenger model doesn't have lat/lng
            current_requests = [p.request for p in ride.passengers if p.status == "ASSIGNED" and p.request]
            all_requests = current_requests + [new_request]

            if self.check_detour_tolerance(all_requests):
                return ride
        return None

    def check_detour_tolerance(self, requests):
        if len(requests) <= 1:
            return True

        # Assume all drops are the same, take the first drop
        drop_lat = requests[0].drop_lat
        drop_lng = requests[0].drop_lng

        # Sort pickups by increasing distance to drop
        # For airport drop, we pick up the furthest person first.
        sorted_requests = sorted(requests, key=lambda r: haversine(r.pickup_lat, r.pickup_lng, drop_lat, drop_lng), reverse=True)

        for i, req in enumerate(sorted_requests):
            direct = haversine(req.pickup_lat, req.pickup_lng, drop_lat, drop_lng)
            shared = 0
            # Sum from this pickup to end
            for j in range(i, len(sorted_requests) - 1):
                shared += haversine(sorted_requests[j].pickup_lat, sorted_requests[j].pickup_lng,
                                    sorted_requests[j+1].pickup_lat, sorted_requests[j+1].pickup_lng)
            shared += haversine(sorted_requests[-1].pickup_lat, sorted_requests[-1].pickup_lng, drop_lat, drop_lng)

            detour_percent = ((shared - direct) / direct) * 100 if direct > 0 else 0
            if detour_percent > req.detour_tolerance_percent:
                return False
        return True
