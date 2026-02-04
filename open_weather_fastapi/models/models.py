from sqlalchemy.orm import relationship
from open_weather_fastapi.core import Base, engine
from sqlalchemy import Column, ForeignKey, Integer, Float, String


class Cities(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    weather = relationship("Weathers", back_populates="city", uselist=False)
    

class Weathers(Base):
    __tablename__ = "weathers"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey('cities.id'), unique=True, nullable=False)
    temperature_2m = Column(Float)
    relative_humidity_2m = Column(Float)
    pressure_msl = Column(Float)
    surface_pressure = Column(Float)
    city = relationship("Cities", back_populates="weather")


Base.metadata.create_all(engine)