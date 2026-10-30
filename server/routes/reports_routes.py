from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from server.config.database import get_db
from server.models import schemas
from server.controllers import reports_controller

router = APIRouter(prefix="/reports", tags=["Reports & Analytics"])

@router.get("/sales", response_model=schemas.SalesSummary)
def get_sales_report(period: str = Query("daily", description="daily, weekly, or monthly"), db: Session = Depends(get_db)):
    return reports_controller.get_sales_report(period, db)

@router.get("/top-items", response_model=List[schemas.TopItem])
def get_top_selling_items(limit: int = 5, db: Session = Depends(get_db)):
    return reports_controller.get_top_selling_items(limit, db)

@router.get("/revenue", response_model=List[schemas.RevenueAnalytics])
def get_revenue_analytics(db: Session = Depends(get_db)):
    return reports_controller.get_revenue_analytics(db)

@router.get("/inventory-consumption", response_model=List[schemas.InventoryConsumption])
def get_inventory_consumption(days: int = 30, db: Session = Depends(get_db)):
    return reports_controller.get_inventory_consumption(days, db)

@router.get("/customers", response_model=List[schemas.CustomerActivity])
def get_customer_activity(limit: int = 5, db: Session = Depends(get_db)):
    return reports_controller.get_customer_activity(limit, db)
