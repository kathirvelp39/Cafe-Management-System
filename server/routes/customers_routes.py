from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from jose import JWTError, jwt

from server.config.database import get_db
from server.models import models, schemas
from server.middleware import auth
from server.controllers import customers_controller

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    user = db.query(models.Customer).filter(models.Customer.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/auth/register", response_model=schemas.CustomerResponse)
def register(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return customers_controller.register_customer(customer, db)

@router.post("/auth/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return customers_controller.login_customer(form_data, db)

@router.post("/auth/reset-password")
def reset_password(reset_data: schemas.PasswordReset, db: Session = Depends(get_db)):
    return customers_controller.reset_password(reset_data, db)

@router.post("/auth/request-otp")
def request_otp(otp_req: schemas.OTPRequest, db: Session = Depends(get_db)):
    from server.services import otp_service
    return otp_service.request_otp_for_customer(otp_req.email, db)

@router.post("/auth/verify-otp", response_model=schemas.Token)
def verify_otp(otp_ver: schemas.OTPVerify, db: Session = Depends(get_db)):
    from server.services import otp_service
    customer = otp_service.verify_customer_otp(otp_ver.email, otp_ver.otp_code, db)
    
    # Generate token
    from server.middleware import auth
    from datetime import timedelta
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": customer.email, "email": customer.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/customers/me", response_model=schemas.CustomerResponse)
def get_my_profile(current_user: models.Customer = Depends(get_current_user)):
    return customers_controller.get_profile(current_user)

@router.get("/customers/me/orders", response_model=List[schemas.OrderResponse])
def get_my_orders(db: Session = Depends(get_db), user: models.Customer = Depends(get_current_user)):
    return customers_controller.get_my_orders(user, db)

@router.get("/customers/me/loyalty", response_model=List[schemas.LoyaltyPointResponse])
def get_my_loyalty_points(db: Session = Depends(get_db), user: models.Customer = Depends(get_current_user)):
    return customers_controller.get_my_loyalty_points(user, db)

@router.post("/customers/me/loyalty", response_model=schemas.LoyaltyPointResponse)
def add_loyalty_points(points: schemas.LoyaltyPointCreate, db: Session = Depends(get_db), user: models.Customer = Depends(get_current_user)):
    return customers_controller.add_loyalty_points(points, user, db)

@router.get("/customers/me/loyalty/total")
def get_total_loyalty_points(db: Session = Depends(get_db), user: models.Customer = Depends(get_current_user)):
    return customers_controller.get_total_loyalty_points(user, db)
