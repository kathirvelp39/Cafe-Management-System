from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from server.config.database import get_db
from server.models import models, schemas
from server.controllers import orders_controller
from server.routes.customers_routes import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("", response_model=schemas.OrderResponse)
def place_order(order_req: schemas.OrderCreate, db: Session = Depends(get_db), user: models.Customer = Depends(get_current_user)):
    return orders_controller.place_order(order_req, user, db)

@router.get("/kitchen/tickets", response_model=List[schemas.OrderResponse])
def get_kitchen_tickets(db: Session = Depends(get_db)):
    return orders_controller.get_kitchen_tickets(db)

@router.get("/{order_id}", response_model=schemas.OrderResponse)
def get_order_status(order_id: int, db: Session = Depends(get_db), user: models.Customer = Depends(get_current_user)):
    return orders_controller.get_order_status(order_id, user, db)

@router.put("/{order_id}/status", response_model=schemas.OrderResponse)
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    return orders_controller.update_order_status(order_id, status, db)

@router.delete("/{order_id}")
def cancel_order(order_id: int, db: Session = Depends(get_db), user: models.Customer = Depends(get_current_user)):
    return orders_controller.cancel_order(order_id, user, db)
