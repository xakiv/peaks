from typing import Union, List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud
from .database import SessionLocal, engine
from .models import Base
from .schemas import PeakCreate, PeakUpdate, Peak

Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/")
def read_root():
    return {"message": "Deak hiker, this is the result of a technical assessment. "}


@app.get("/api/peaks/", response_model=List[Peak])
def list_peaks(
    bbox: Union[str, None] = None,
    db: Session = Depends(get_db),
):
    """
    List peaks.
    Args:
        bbox (str, optional): An optional bounding box coordinates in 4326 projection.
        This allows retrieve a list of peaks in a given geographical bounding box. EX: "bbox=-2.526855,41.153842,3.328857,43.596306"
    Returns:
        list: A list of dictionaries items details.
    """
    return crud.get_peaks(db, bbox)


@app.get("/api/peaks/{peak_id}", response_model=Peak)
def read_peak(peak_id: int, db: Session = Depends(get_db)):
    """
    Retrieve peaks detail.
    Args:
        peak_id (int): The ID of the item to retrieve.
    Returns:
        dict: A dictionary with item details
    """
    db_peak = crud.get_peak(db, peak_id=peak_id)
    if db_peak is None:
        raise HTTPException(status_code=404, detail="Peak not found")
    return db_peak


@app.delete("/api/peaks/{peak_id}")
def delete_peak(peak_id: int, db: Session = Depends(get_db)):
    db_peak = crud.get_peak(db, peak_id=peak_id)
    if db_peak is None:
        raise HTTPException(status_code=404, detail="Peak not found")
    return crud.delete_peak(db, db_peak)


@app.put("/api/peaks/{peak_id}", response_model=Peak)
def update_peak(peak_id: int, peak: PeakUpdate, db: Session = Depends(get_db)):
    db_peak = crud.get_peak(db, peak_id=peak_id)
    if db_peak is None:
        raise HTTPException(status_code=404, detail="Peak not found")
    return crud.update_peak(db, db_peak, peak)


@app.post("/api/peaks/", response_model=Peak, status_code=201)
def create_peak(peak: PeakCreate, db: Session = Depends(get_db)):
    return crud.create_peak(db, peak)
