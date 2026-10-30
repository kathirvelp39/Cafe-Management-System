from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from server.models import schemas
from server.services import customers_service

def register_customer(customer: schemas.CustomerCreate, db: Session):
    return customers_service.create_customer(customer, db)

def login_customer(form_data: OAuth2PasswordRequestForm, db: Session):
    return customers_service.authenticate_customer(form_data, db)

def reset_password(reset_data: schemas.PasswordReset, db: Session):
    return customers_service.reset_password(reset_data, db)

def get_profile(current_user):
    return current_user

def get_my_orders(user, db: Session):
    return customers_service.get_orders(user.id, db)

def get_my_loyalty_points(user, db: Session):
    return customers_service.get_loyalty_points(user.id, db)

def add_loyalty_points(points: schemas.LoyaltyPointCreate, user, db: Session):
    return customers_service.add_loyalty_points(user.id, points, db)

def get_total_loyalty_points(user, db: Session):
    return customers_service.get_total_loyalty_points(user.id, db)
