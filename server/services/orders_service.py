from sqlalchemy.orm import Session
from server.models import models, schemas
from fastapi import HTTPException

def place_order(order_req: schemas.OrderCreate, user_id: int, db: Session):
    total_amount = 0.0
    menu_items = []
    
    for item_req in order_req.items:
        menu_item = db.query(models.MenuItem).filter(models.MenuItem.id == item_req.menu_item_id).first()
        if not menu_item:
            raise HTTPException(status_code=404, detail=f"Menu item {item_req.menu_item_id} not found")
        if not menu_item.is_available:
            raise HTTPException(status_code=400, detail=f"Menu item {menu_item.name} is currently unavailable")
        
        total_amount += menu_item.price * item_req.quantity
        menu_items.append((menu_item, item_req.quantity))
        
    new_order = models.Order(
        customer_id=user_id,
        order_type=order_req.order_type,
        table_number=order_req.table_number,
        status="Pending",
        total_amount=total_amount
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    for menu_item, quantity in menu_items:
        order_item = models.OrderItem(
            order_id=new_order.id,
            menu_item_id=menu_item.id,
            quantity=quantity,
            unit_price=menu_item.price
        )
        db.add(order_item)
        
    db.commit()
    db.refresh(new_order)
    return new_order

def get_kitchen_tickets(db: Session):
    active_statuses = ["Pending", "Preparing"]
    return db.query(models.Order).filter(models.Order.status.in_(active_statuses)).all()

def get_order_status(order_id: int, user_id: int, db: Session):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.customer_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this order")
        
    return order

def update_order_status(order_id: int, status: str, db: Session):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    valid_statuses = ["Pending", "Preparing", "Ready", "Completed", "Cancelled"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of {valid_statuses}")
        
    order.status = status
    db.commit()
    db.refresh(order)
    return order

def cancel_order(order_id: int, user_id: int, db: Session):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    if order.customer_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to cancel this order")
        
    if order.status != "Pending":
        raise HTTPException(status_code=400, detail="Order cannot be cancelled because it is already being prepared or completed.")
        
    order.status = "Cancelled"
    db.commit()
    return {"message": "Order has been cancelled successfully"}
