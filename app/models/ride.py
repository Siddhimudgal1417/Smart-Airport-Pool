from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Ride(Base):
    __tablename__ = "rides"

    id = Column(Integer, primary_key=True)
    cab_id = Column(Integer, ForeignKey("cabs.id"))
    status = Column(String, default="ONGOING")
    passengers = relationship("RideRequest", backref="ride")
