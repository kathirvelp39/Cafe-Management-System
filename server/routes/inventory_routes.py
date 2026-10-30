from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from server.config.database import get_db
from server.models import schemas
from server.controllers import inventory_controller

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.post("/suppliers", response_model=schemas.SupplierResponse)
def add_supplier(supplier: schemas.SupplierCreate, db: Session = Depends(get_db)):
    return inventory_controller.add_supplier(supplier, db)

@router.get("/suppliers", response_model=List[schemas.SupplierResponse])
def get_suppliers(db: Session = Depends(get_db)):
    return inventory_controller.get_suppliers(db)

@router.post("/ingredients", response_model=schemas.IngredientResponse)
def add_ingredient(ingredient: schemas.IngredientCreate, db: Session = Depends(get_db)):
    return inventory_controller.add_ingredient(ingredient, db)

@router.get("/ingredients", response_model=List[schemas.IngredientResponse])
def get_ingredients(db: Session = Depends(get_db)):
    return inventory_controller.get_ingredients(db)

@router.post("/ingredients/{ingredient_id}/stock", response_model=schemas.StockTransactionResponse)
def update_stock(ingredient_id: int, transaction: schemas.StockTransactionCreate, db: Session = Depends(get_db)):
    return inventory_controller.update_stock(ingredient_id, transaction, db)

@router.get("/ingredients/{ingredient_id}/history", response_model=List[schemas.StockTransactionResponse])
def get_stock_history(ingredient_id: int, db: Session = Depends(get_db)):
    return inventory_controller.get_stock_history(ingredient_id, db)

@router.get("/alerts/low-stock", response_model=List[schemas.IngredientResponse])
def get_low_stock_alerts(db: Session = Depends(get_db)):
    return inventory_controller.get_low_stock_alerts(db)
