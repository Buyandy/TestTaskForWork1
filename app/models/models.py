from sqlalchemy.orm import relationship
from ..core import Base, engine
from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime
from ..tools.get_time import now_time


class Cities(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    weather = relationship("Weathers", back_populates="city", uselist=False)
    created_at = Column(DateTime, default=now_time, nullable=False)
    

class Weathers(Base):
    __tablename__ = "weathers"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey('cities.id'), unique=True, nullable=False)
    temperature_2m = Column(Float)
    relative_humidity_2m = Column(Float)
    pressure_msl = Column(Float)
    surface_pressure = Column(Float)
    city = relationship("Cities", back_populates="weather")
    created_at = Column(DateTime(timezone=True), default=now_time, nullable=False)
    updated_at = Column(
        DateTime(timezone=True), 
        default=now_time, 
        onupdate=now_time, 
        nullable=False
    )


Base.metadata.create_all(engine)