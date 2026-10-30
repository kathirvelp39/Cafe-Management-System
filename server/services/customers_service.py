from sqlalchemy.orm import Session
from server.models import models, schemas
from server.middleware import auth
from fastapi import HTTPException

def create_customer(customer: schemas.CustomerCreate, db: Session):
    if db.query(models.Customer).filter(models.Customer.email == customer.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pwd = auth.get_password_hash(customer.password)
    new_customer = models.Customer(email=customer.email, full_name=customer.full_name, hashed_password=hashed_pwd)
    
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

def authenticate_customer(form_data, db: Session):
    user = db.query(models.Customer).filter(models.Customer.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    from datetime import timedelta
    token = auth.create_access_token({"email": user.email}, timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}

def reset_password(reset_data: schemas.PasswordReset, db: Session):
    user = db.query(models.Customer).filter(models.Customer.email == reset_data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    user.hashed_password = auth.get_password_hash(reset_data.new_password)
    db.commit()
    return {"message": "Password updated successfully"}

def get_orders(user_id: int, db: Session):
    return db.query(models.Order).filter(models.Order.customer_id == user_id).all()

def get_loyalty_points(user_id: int, db: Session):
    return db.query(models.LoyaltyPoint).filter(models.LoyaltyPoint.customer_id == user_id).all()

def add_loyalty_points(user_id: int, points: schemas.LoyaltyPointCreate, db: Session):
    new_points = models.LoyaltyPoint(**points.model_dump(), customer_id=user_id)
    db.add(new_points)
    db.commit()
    db.refresh(new_points)
    return new_points

def get_total_loyalty_points(user_id: int, db: Session):
    points_list = db.query(models.LoyaltyPoint).filter(models.LoyaltyPoint.customer_id == user_id).all()
    total = sum(p.points for p in points_list)
    return {"total_points": total}
