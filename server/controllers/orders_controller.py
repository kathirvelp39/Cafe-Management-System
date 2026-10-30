from sqlalchemy.orm import Session
from server.models import schemas
from server.services import orders_service

def place_order(order_req: schemas.OrderCreate, user, db: Session):
    return orders_service.place_order(order_req, user.id, db)

def get_kitchen_tickets(db: Session):
    return orders_service.get_kitchen_tickets(db)

def get_order_status(order_id: int, user, db: Session):
    return orders_service.get_order_status(order_id, user.id, db)

def update_order_status(order_id: int, status: str, db: Session):
    return orders_service.update_order_status(order_id, status, db)

def cancel_order(order_id: int, user, db: Session):
    return orders_service.cancel_order(order_id, user.id, db)
