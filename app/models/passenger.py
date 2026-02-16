from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Passenger(Base):
    __tablename__ = "passengers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    luggage_units = Column(Integer, default=0)
