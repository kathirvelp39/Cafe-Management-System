from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from server.config.database import get_db
from server.models import schemas
from server.controllers import reservations_controller

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.post("/tables", response_model=schemas.TableResponse)
def add_table(table: schemas.TableCreate, db: Session = Depends(get_db)):
    return reservations_controller.add_table(table, db)

@router.get("/tables", response_model=List[schemas.TableResponse])
def get_tables(db: Session = Depends(get_db)):
    return reservations_controller.get_tables(db)

@router.get("/availability", response_model=List[schemas.TableResponse])
def check_availability(time: datetime, guests: int = Query(..., gt=0), db: Session = Depends(get_db)):
    return reservations_controller.check_availability(time, guests, db)

@router.post("", response_model=schemas.ReservationResponse)
def book_table(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    return reservations_controller.book_table(reservation, db)

@router.get("", response_model=List[schemas.ReservationResponse])
def get_reservations(db: Session = Depends(get_db)):
    return reservations_controller.get_reservations(db)

@router.put("/{reservation_id}/status", response_model=schemas.ReservationResponse)
def update_reservation_status(reservation_id: int, status_update: schemas.ReservationUpdate, db: Session = Depends(get_db)):
    return reservations_controller.update_reservation_status(reservation_id, status_update, db)
