from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Cab(Base):
    __tablename__ = "cabs"

    id = Column(Integer, primary_key=True, index=True)
    seat_capacity = Column(Integer, nullable=False)
    available_seats = Column(Integer, nullable=False)
    luggage_capacity = Column(Integer, nullable=False)
    available_luggage = Column(Integer, nullable=False)
    status = Column(String, default="ACTIVE")
