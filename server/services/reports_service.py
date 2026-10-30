from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from fastapi import HTTPException
from datetime import datetime, timedelta
from server.models import models, schemas

def get_sales_report(period: str, db: Session):
    now = datetime.utcnow()
    if period == "daily":
        start_date = now - timedelta(days=1)
    elif period == "weekly":
        start_date = now - timedelta(weeks=1)
    elif period == "monthly":
        start_date = now - timedelta(days=30)
    else:
        raise HTTPException(status_code=400, detail="Invalid period. Use daily, weekly, or monthly.")
        
    result = db.query(
        func.count(models.Order.id).label("total_orders"),
        func.sum(models.Order.total_amount).label("total_revenue")
    ).filter(models.Order.created_at >= start_date, models.Order.status != "Cancelled").first()
    
    total_orders = result.total_orders or 0
    total_revenue = result.total_revenue or 0.0
    average_order_value = total_revenue / total_orders if total_orders > 0 else 0.0
    
    return schemas.SalesSummary(
        period=period,
        total_orders=total_orders,
        total_revenue=total_revenue,
        average_order_value=round(average_order_value, 2)
    )

def get_top_selling_items(limit: int, db: Session):
    results = db.query(
        models.OrderItem.menu_item_id,
        models.MenuItem.name,
        func.sum(models.OrderItem.quantity).label("total_quantity_sold")
    ).join(models.MenuItem, models.OrderItem.menu_item_id == models.MenuItem.id)\
     .group_by(models.OrderItem.menu_item_id, models.MenuItem.name)\
     .order_by(desc("total_quantity_sold"))\
     .limit(limit).all()
     
    return [schemas.TopItem(menu_item_id=r.menu_item_id, name=r.name, total_quantity_sold=r.total_quantity_sold) for r in results]

def get_revenue_analytics(db: Session):
    results = db.query(
        models.Invoice.payment_method,
        func.sum(models.Invoice.total_amount).label("total_revenue")
    ).filter(models.Invoice.payment_status == "Paid", models.Invoice.payment_method.isnot(None))\
     .group_by(models.Invoice.payment_method).all()
     
    return [schemas.RevenueAnalytics(payment_method=r.payment_method, total_revenue=r.total_revenue) for r in results]

def get_inventory_consumption(days: int, db: Session):
    start_date = datetime.utcnow() - timedelta(days=days)
    
    results = db.query(
        models.StockTransaction.ingredient_id,
        models.Ingredient.name,
        models.Ingredient.unit,
        func.sum(models.StockTransaction.quantity).label("total_consumed")
    ).join(models.Ingredient, models.StockTransaction.ingredient_id == models.Ingredient.id)\
     .filter(models.StockTransaction.transaction_type == "OUT", models.StockTransaction.created_at >= start_date)\
     .group_by(models.StockTransaction.ingredient_id, models.Ingredient.name, models.Ingredient.unit)\
     .order_by(desc("total_consumed")).all()
     
    return [
        schemas.InventoryConsumption(
            ingredient_id=r.ingredient_id, 
            name=r.name, 
            total_consumed=r.total_consumed, 
            unit=r.unit
        ) for r in results
    ]

def get_customer_activity(limit: int, db: Session):
    results = db.query(
        models.Order.customer_id,
        models.Customer.full_name,
        func.count(models.Order.id).label("total_orders"),
        func.sum(models.Order.total_amount).label("total_spent")
    ).join(models.Customer, models.Order.customer_id == models.Customer.id)\
     .group_by(models.Order.customer_id, models.Customer.full_name)\
     .order_by(desc("total_spent"))\
     .limit(limit).all()
     
    return [
        schemas.CustomerActivity(
            customer_id=r.customer_id,
            full_name=r.full_name,
            total_orders=r.total_orders,
            total_spent=r.total_spent
        ) for r in results
    ]
