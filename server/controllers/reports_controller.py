from sqlalchemy.orm import Session
from server.services import reports_service

def get_sales_report(period: str, db: Session):
    return reports_service.get_sales_report(period, db)

def get_top_selling_items(limit: int, db: Session):
    return reports_service.get_top_selling_items(limit, db)

def get_revenue_analytics(db: Session):
    return reports_service.get_revenue_analytics(db)

def get_inventory_consumption(days: int, db: Session):
    return reports_service.get_inventory_consumption(days, db)

def get_customer_activity(limit: int, db: Session):
    return reports_service.get_customer_activity(limit, db)
