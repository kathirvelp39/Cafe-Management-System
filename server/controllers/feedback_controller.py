from sqlalchemy.orm import Session
from typing import Optional
from server.models import schemas
from server.services import feedback_service

def submit_feedback(feedback: schemas.FeedbackCreate, db: Session):
    return feedback_service.submit_feedback(feedback, db)

def get_feedback(is_complaint: Optional[bool], status: Optional[str], db: Session):
    return feedback_service.get_feedback(is_complaint, status, db)

def resolve_complaint(feedback_id: int, update_data: schemas.FeedbackUpdate, db: Session):
    return feedback_service.resolve_complaint(feedback_id, update_data, db)
