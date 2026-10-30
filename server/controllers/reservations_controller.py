from sqlalchemy.orm import Session
from datetime import datetime
from server.models import schemas
from server.services import reservations_service

def add_table(table: schemas.TableCreate, db: Session):
    return reservations_service.add_table(table, db)

def get_tables(db: Session):
    return reservations_service.get_tables(db)

def check_availability(time: datetime, guests: int, db: Session):
    return reservations_service.check_availability(time, guests, db)

def book_table(reservation: schemas.ReservationCreate, db: Session):
    return reservations_service.book_table(reservation, db)

def get_reservations(db: Session):
    return reservations_service.get_reservations(db)

def update_reservation_status(reservation_id: int, status_update: schemas.ReservationUpdate, db: Session):
    return reservations_service.update_reservation_status(reservation_id, status_update, db)
