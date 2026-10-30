from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from server.config.database import get_db
from server.models import schemas
from server.controllers import feedback_controller

router = APIRouter(prefix="/feedback", tags=["Feedback & Reviews"])

@router.post("", response_model=schemas.FeedbackResponse)
def submit_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    return feedback_controller.submit_feedback(feedback, db)

@router.get("", response_model=List[schemas.FeedbackResponse])
def get_feedback(is_complaint: Optional[bool] = None, status: Optional[str] = None, db: Session = Depends(get_db)):
    return feedback_controller.get_feedback(is_complaint, status, db)

@router.put("/{feedback_id}/resolve", response_model=schemas.FeedbackResponse)
def resolve_complaint(feedback_id: int, update_data: schemas.FeedbackUpdate, db: Session = Depends(get_db)):
    return feedback_controller.resolve_complaint(feedback_id, update_data, db)
