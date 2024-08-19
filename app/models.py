from sqlalchemy import Column, Integer, String, Numeric
from geoalchemy2 import Geography

from .database import Base


class Peak(Base):
    __tablename__ = "peaks"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    altitude = Column(Numeric)
    lon = Column(Numeric)
    lat = Column(Numeric)
    geom = Column(Geography("POINT", srid=4326))
