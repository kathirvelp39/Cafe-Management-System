from sqlalchemy.orm import Session
from server.models import schemas
from server.services import inventory_service

def add_supplier(supplier: schemas.SupplierCreate, db: Session):
    return inventory_service.add_supplier(supplier, db)

def get_suppliers(db: Session):
    return inventory_service.get_suppliers(db)

def add_ingredient(ingredient: schemas.IngredientCreate, db: Session):
    return inventory_service.add_ingredient(ingredient, db)

def get_ingredients(db: Session):
    return inventory_service.get_ingredients(db)

def update_stock(ingredient_id: int, transaction: schemas.StockTransactionCreate, db: Session):
    return inventory_service.update_stock(ingredient_id, transaction, db)

def get_stock_history(ingredient_id: int, db: Session):
    return inventory_service.get_stock_history(ingredient_id, db)

def get_low_stock_alerts(db: Session):
    return inventory_service.get_low_stock_alerts(db)
