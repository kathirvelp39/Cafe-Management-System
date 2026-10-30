from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timedelta
from server.models import models, schemas

def add_table(table: schemas.TableCreate, db: Session):
    existing_table = db.query(models.RestaurantTable).filter(models.RestaurantTable.table_number == table.table_number).first()
    if existing_table:
        raise HTTPException(status_code=400, detail="Table number already exists")
        
    new_table = models.RestaurantTable(**table.model_dump())
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    return new_table

def get_tables(db: Session):
    return db.query(models.RestaurantTable).all()

def check_availability(time: datetime, guests: int, db: Session):
    window_start = time - timedelta(hours=2)
    window_end = time + timedelta(hours=2)
    
    booked_tables = db.query(models.Reservation.table_id).filter(
        models.Reservation.status.in_(["Pending", "Approved"]),
        models.Reservation.reservation_time > window_start,
        models.Reservation.reservation_time < window_end
    ).subquery()
    
    available_tables = db.query(models.RestaurantTable).filter(
        models.RestaurantTable.is_active == True,
        models.RestaurantTable.capacity >= guests,
        ~models.RestaurantTable.id.in_(booked_tables)
    ).all()
    
    return available_tables

def book_table(reservation: schemas.ReservationCreate, db: Session):
    customer = db.query(models.Customer).filter(models.Customer.id == reservation.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
        
    table = db.query(models.RestaurantTable).filter(models.RestaurantTable.id == reservation.table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    if table.capacity < reservation.number_of_guests:
        raise HTTPException(status_code=400, detail="Table capacity is too small for this party")
        
    window_start = reservation.reservation_time - timedelta(hours=2)
    window_end = reservation.reservation_time + timedelta(hours=2)
    
    conflicting_booking = db.query(models.Reservation).filter(
        models.Reservation.table_id == reservation.table_id,
        models.Reservation.status.in_(["Pending", "Approved"]),
        models.Reservation.reservation_time > window_start,
        models.Reservation.reservation_time < window_end
    ).first()
    
    if conflicting_booking:
        raise HTTPException(status_code=400, detail="Table is already booked during this time window")
        
    new_reservation = models.Reservation(**reservation.model_dump())
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return new_reservation

def get_reservations(db: Session):
    return db.query(models.Reservation).all()

def update_reservation_status(reservation_id: int, status_update: schemas.ReservationUpdate, db: Session):
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
        
    valid_statuses = ["Pending", "Approved", "Cancelled", "Completed"]
    if status_update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of {valid_statuses}")
        
    reservation.status = status_update.status
    db.commit()
    db.refresh(reservation)
    return reservation
