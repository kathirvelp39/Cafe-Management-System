from sqlalchemy.orm import Session
from server.models import schemas
from server.services import billing_service

def generate_invoice(order_id: int, db: Session):
    return billing_service.generate_invoice(order_id, db)

def process_payment(invoice_id: int, payment_req: schemas.PaymentRequest, db: Session):
    return billing_service.process_payment(invoice_id, payment_req, db)

def download_invoice(invoice_id: int, db: Session):
    return billing_service.download_invoice(invoice_id, db)

def email_invoice(invoice_id: int, db: Session):
    return billing_service.email_invoice(invoice_id, db)
