from pydantic import BaseModel, ConfigDict
from pydantic_extra_types.coordinate import Longitude, Latitude


class PeakBase(BaseModel):
    name: str
    altitude: float
    lon: Longitude
    lat: Latitude


class PeakCreate(PeakBase):
    pass


class Peak(PeakBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    altitude: float
    lon: Longitude
    lat: Latitude


class PeakUpdate(BaseModel):
    name: str
    altitude: float
    lon: Longitude
    lat: Latitude
