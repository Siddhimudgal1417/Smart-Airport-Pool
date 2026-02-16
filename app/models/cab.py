from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Cab(Base):
    __tablename__ = "cabs"
    id = Column(Integer, primary_key=True, index=True)
    driver_name = Column(String)
    license_plate = Column(String)
    capacity = Column(Integer)
    available_seats = Column(Integer)
    available_luggage = Column(Integer)
    status = Column(String, default="ACTIVE")
    current_lat = Column(Float)
    current_lng = Column(Float)