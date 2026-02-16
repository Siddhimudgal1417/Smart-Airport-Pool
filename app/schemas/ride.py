from pydantic import BaseModel

class RideRequestCreate(BaseModel):
    passenger_id: int
    pickup_lat: float
    pickup_lng: float
    drop_lat: float
    drop_lng: float
    detour_tolerance_percent: float
