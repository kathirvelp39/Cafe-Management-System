from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.config.database import get_db
from server.models import schemas
from server.controllers import billing_controller

router = APIRouter(prefix="/billing", tags=["Billing"])

@router.post("/generate/{order_id}", response_model=schemas.InvoiceResponse)
def generate_invoice(order_id: int, db: Session = Depends(get_db)):
    return billing_controller.generate_invoice(order_id, db)

@router.post("/pay/{invoice_id}", response_model=schemas.InvoiceResponse)
def process_payment(invoice_id: int, payment_req: schemas.PaymentRequest, db: Session = Depends(get_db)):
    return billing_controller.process_payment(invoice_id, payment_req, db)

@router.get("/invoice/{invoice_id}/download")
def download_invoice(invoice_id: int, db: Session = Depends(get_db)):
    return billing_controller.download_invoice(invoice_id, db)

@router.post("/invoice/{invoice_id}/email")
def email_invoice(invoice_id: int, db: Session = Depends(get_db)):
    return billing_controller.email_invoice(invoice_id, db)
