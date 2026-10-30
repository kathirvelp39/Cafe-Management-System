from sqlalchemy.orm import Session
from fastapi import HTTPException
from server.models import models, schemas
from typing import Optional

def submit_feedback(feedback: schemas.FeedbackCreate, db: Session):
    customer = db.query(models.Customer).filter(models.Customer.id == feedback.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
        
    if feedback.order_id:
        order = db.query(models.Order).filter(models.Order.id == feedback.order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
            
    new_feedback = models.Feedback(**feedback.model_dump())
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback

def get_feedback(is_complaint: Optional[bool], status: Optional[str], db: Session):
    query = db.query(models.Feedback)
    
    if is_complaint is not None:
        query = query.filter(models.Feedback.is_complaint == is_complaint)
        
    if status:
        query = query.filter(models.Feedback.status == status)
        
    return query.all()

def resolve_complaint(feedback_id: int, update_data: schemas.FeedbackUpdate, db: Session):
    feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
        
    if not feedback.is_complaint:
        raise HTTPException(status_code=400, detail="Only flagged complaints need resolution workflows")
        
    valid_statuses = ["Pending", "Investigating", "Resolved"]
    if update_data.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of {valid_statuses}")
        
    feedback.status = update_data.status
    feedback.resolution_notes = update_data.resolution_notes
    db.commit()
    db.refresh(feedback)
    
    if feedback.status == "Resolved" and feedback.customer:
        from server.services.email_service import send_email
        subject = f"Update on your recent feedback (Order #{feedback.order_id or 'N/A'})"
        body = f"Dear {feedback.customer.full_name},\n\nWe have reviewed your recent feedback. Here is the resolution from our management team:\n\n{feedback.resolution_notes}\n\nThank you for helping us improve Monika G Cafe!\n\nBest,\nManagement Team"
        send_email(to_email=feedback.customer.email, subject=subject, body=body)
        
    return feedback
