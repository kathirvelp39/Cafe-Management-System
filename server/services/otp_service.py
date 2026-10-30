import random
import string
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException
from server.models import models
from server.services.email_service import send_email

def generate_otp_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

def request_otp_for_customer(email: str, db: Session):
    customer = db.query(models.Customer).filter(models.Customer.email == email).first()
    if not customer:
        # We still return success to prevent email enumeration, but we don't send an email.
        return {"message": "If the email is registered, an OTP has been sent."}

    otp_code = generate_otp_code()
    
    # Store OTP and set expiry to 5 minutes from now
    customer.otp_code = otp_code
    customer.otp_expiry = datetime.now(timezone.utc) + timedelta(minutes=5)
    
    db.commit()

    # Send email
    subject = "Your Monika G Cafe One-Time Password (OTP)"
    body = f"Hello {customer.full_name},\n\nYour One-Time Password is: {otp_code}\n\nThis code will expire in 5 minutes.\n\nIf you did not request this, please ignore this email.\n\nBest regards,\nMonika G Cafe Security Team"
    
    try:
        send_email(to_email=customer.email, subject=subject, body=body)
    except Exception as e:
        print(f"Error sending OTP email: {e}")
        # In a real system, you might want to handle this gracefully
        pass

    return {"message": "If the email is registered, an OTP has been sent."}

def verify_customer_otp(email: str, otp_code: str, db: Session):
    customer = db.query(models.Customer).filter(models.Customer.email == email).first()
    
    if not customer:
        raise HTTPException(status_code=401, detail="Invalid email or OTP")
        
    if not customer.otp_code or customer.otp_code != otp_code:
        raise HTTPException(status_code=401, detail="Invalid OTP code")
        
    # Check expiry
    # Note: SQLite stores datetime without timezone by default, MySQL might have different behaviors.
    # We compare offset-naive or offset-aware properly. 
    now = datetime.now(timezone.utc)
    # Ensure customer.otp_expiry is aware for comparison
    expiry = customer.otp_expiry
    if expiry.tzinfo is None:
        expiry = expiry.replace(tzinfo=timezone.utc)
        
    if now > expiry:
        raise HTTPException(status_code=401, detail="OTP code has expired")
        
    # OTP is valid! Clear it so it can't be reused
    customer.otp_code = None
    customer.otp_expiry = None
    db.commit()
    
    return customer
