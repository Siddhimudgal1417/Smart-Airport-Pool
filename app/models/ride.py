from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Ride(Base):
    __tablename__ = "rides"
    id = Column(Integer, primary_key=True, index=True)
    cab_id = Column(Integer, ForeignKey("cabs.id"))
    status = Column(String, default="ONGOING")
    
    cab = relationship("app.models.cab.Cab")
    passengers = relationship("app.models.passenger.Passenger", back_populates="ride")