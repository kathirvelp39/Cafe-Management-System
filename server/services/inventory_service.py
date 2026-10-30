from sqlalchemy.orm import Session
from fastapi import HTTPException
from server.models import models, schemas

def add_supplier(supplier: schemas.SupplierCreate, db: Session):
    new_supplier = models.Supplier(**supplier.model_dump())
    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)
    return new_supplier

def get_suppliers(db: Session):
    return db.query(models.Supplier).all()

def add_ingredient(ingredient: schemas.IngredientCreate, db: Session):
    if ingredient.supplier_id:
        supplier = db.query(models.Supplier).filter(models.Supplier.id == ingredient.supplier_id).first()
        if not supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")
            
    new_ingredient = models.Ingredient(**ingredient.model_dump())
    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)
    return new_ingredient

def get_ingredients(db: Session):
    return db.query(models.Ingredient).all()

def update_stock(ingredient_id: int, transaction: schemas.StockTransactionCreate, db: Session):
    ingredient = db.query(models.Ingredient).filter(models.Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
        
    if transaction.transaction_type not in ["IN", "OUT"]:
        raise HTTPException(status_code=400, detail="Transaction type must be 'IN' or 'OUT'")
        
    if transaction.transaction_type == "OUT" and ingredient.stock_level < transaction.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock to consume this amount")
        
    new_transaction = models.StockTransaction(
        ingredient_id=ingredient_id,
        transaction_type=transaction.transaction_type,
        quantity=transaction.quantity,
        remarks=transaction.remarks
    )
    db.add(new_transaction)
    
    if transaction.transaction_type == "IN":
        ingredient.stock_level += transaction.quantity
    else:
        ingredient.stock_level -= transaction.quantity
        
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

def get_stock_history(ingredient_id: int, db: Session):
    ingredient = db.query(models.Ingredient).filter(models.Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
        
    return db.query(models.StockTransaction).filter(models.StockTransaction.ingredient_id == ingredient_id).all()

def get_low_stock_alerts(db: Session):
    return db.query(models.Ingredient).filter(models.Ingredient.stock_level <= models.Ingredient.minimum_stock_level).all()
