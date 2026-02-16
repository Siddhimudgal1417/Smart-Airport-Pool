from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Passenger(Base):
    __tablename__ = "passengers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    luggage_units = Column(Integer, default=1)
    ride_id = Column(Integer, ForeignKey("rides.id"), nullable=True)
    request_id = Column(Integer, ForeignKey("ride_requests.id"), nullable=True)
    status = Column(String, default="IDLE")
    
    ride = relationship("app.models.ride.Ride", back_populates="passengers")
    request = relationship("app.models.ride_request.RideRequest")