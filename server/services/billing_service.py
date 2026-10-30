from sqlalchemy.orm import Session
from fastapi import HTTPException, Response
from server.models import models, schemas
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

TAX_RATE = 0.05

def generate_invoice(order_id: int, db: Session):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    existing_invoice = db.query(models.Invoice).filter(models.Invoice.order_id == order_id).first()
    if existing_invoice:
        return existing_invoice
        
    subtotal = order.total_amount
    tax_amount = round(subtotal * TAX_RATE, 2)
    total_amount = subtotal + tax_amount
    
    new_invoice = models.Invoice(
        order_id=order_id,
        subtotal=subtotal,
        tax_amount=tax_amount,
        total_amount=total_amount,
        payment_status="Pending"
    )
    
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    return new_invoice

def process_payment(invoice_id: int, payment_req: schemas.PaymentRequest, db: Session):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
        
    if invoice.payment_status == "Paid":
        raise HTTPException(status_code=400, detail="Invoice is already paid")
        
    valid_methods = ["Cash", "UPI", "Card"]
    if payment_req.payment_method not in valid_methods:
        raise HTTPException(status_code=400, detail=f"Invalid payment method. Choose from {valid_methods}")
        
    invoice.payment_method = payment_req.payment_method
    invoice.payment_status = "Paid"
    db.commit()
    db.refresh(invoice)
    
    return invoice

def download_invoice(invoice_id: int, db: Session):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
        
    order = db.query(models.Order).filter(models.Order.id == invoice.order_id).first()
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    p.setFont("Helvetica-Bold", 20)
    p.drawString(200, 750, "INVOICE")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, 700, f"Invoice ID: {invoice.id}")
    p.drawString(50, 680, f"Order ID: {order.id}")
    p.drawString(50, 660, f"Order Type: {order.order_type}")
    if order.table_number:
        p.drawString(50, 640, f"Table Number: {order.table_number}")
        
    p.drawString(50, 600, "Items:")
    y = 580
    for item in order.items:
        p.drawString(70, y, f"- {item.menu_item.name} x {item.quantity} : ${item.unit_price * item.quantity:.2f}")
        y -= 20
        
    p.drawString(50, y - 20, f"Subtotal: ${invoice.subtotal:.2f}")
    p.drawString(50, y - 40, f"Tax (5% GST): ${invoice.tax_amount:.2f}")
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y - 70, f"Total Amount: ${invoice.total_amount:.2f}")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, y - 110, f"Payment Status: {invoice.payment_status}")
    if invoice.payment_method:
        p.drawString(50, y - 130, f"Payment Method: {invoice.payment_method}")
        
    p.showPage()
    p.save()
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return Response(
        content=pdf_bytes, 
        media_type="application/pdf", 
        headers={"Content-Disposition": f"attachment; filename=invoice_{invoice.id}.pdf"}
    )

def email_invoice(invoice_id: int, db: Session):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    order = db.query(models.Order).filter(models.Order.id == invoice.order_id).first()
    customer = db.query(models.Customer).filter(models.Customer.id == order.customer_id).first()
    
    if not customer or not customer.email:
        raise HTTPException(status_code=400, detail="Customer email not found")

    # Generate PDF to a temp file
    import tempfile
    import os
    
    pdf_response = download_invoice(invoice_id, db)
    pdf_bytes = pdf_response.body
    
    temp_pdf_path = os.path.join(tempfile.gettempdir(), f"invoice_{invoice.id}.pdf")
    with open(temp_pdf_path, 'wb') as f:
        f.write(pdf_bytes)
        
    try:
        from server.services.email_service import send_email
        subject = f"Your Invoice from Monika G Cafe (Order #{order.id})"
        body = f"Dear {customer.full_name},\n\nThank you for dining with Monika G Cafe! Please find your invoice attached.\n\nTotal Amount: ${invoice.total_amount:.2f}\nStatus: {invoice.payment_status}\n\nWe hope to see you again soon!\n\nBest,\nMonika G Cafe"
        send_email(to_email=customer.email, subject=subject, body=body, attachment_path=temp_pdf_path)
    finally:
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)
            
    return {"message": f"Invoice emailed to {customer.email}"}
