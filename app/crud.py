from typing import Union

from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_MakeEnvelope

from . import models, schemas


def get_peaks(
    db: Session,
    bbox: Union[str, None] = None,
):
    if bbox:
        coords = bbox.split(",")
        coords.append(4326)
        polygon = ST_MakeEnvelope(*coords)
        return db.query(models.Peak).filter(models.Peak.geom.intersects(polygon)).all()
    else:
        return db.query(models.Peak).all()


def get_peak(db: Session, peak_id: int = 0):
    return db.query(models.Peak).filter(models.Peak.id == peak_id).first()


def create_peak(db: Session, peak: schemas.PeakCreate):
    new_row = models.Peak(
        name=peak.name,
        altitude=peak.altitude,
        lon=peak.lon,
        lat=peak.lat,
        geom=f"POINT({peak.lon} {peak.lat})",
    )
    db.add(new_row)
    db.commit()
    db.refresh(new_row)

    return new_row


def update_peak(db: Session, db_peak: models.Peak, peak: schemas.PeakUpdate):
    for k, v in peak.model_dump(exclude_unset=True).items():
        setattr(db_peak, k, v)
    db.commit()
    db.refresh(db_peak)
    return db_peak


def delete_peak(db: Session, peak: models.Peak):
    db.delete(peak)
    db.commit()
    return {"detail": "Peak deleted"}
