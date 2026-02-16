from sqlalchemy import Column, Integer, Float, String, ForeignKey
from app.db.base import Base

class RideRequest(Base):
    __tablename__ = "ride_requests"

    id = Column(Integer, primary_key=True)
    passenger_id = Column(Integer, ForeignKey("passengers.id"))
    pickup_lat = Column(Float)
    pickup_lng = Column(Float)
    drop_lat = Column(Float)
    drop_lng = Column(Float)
    detour_tolerance_percent = Column(Float)
    status = Column(String, default="PENDING")
