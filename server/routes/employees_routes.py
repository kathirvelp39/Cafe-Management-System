from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from server.config.database import get_db
from server.models import schemas
from server.controllers import employees_controller

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.post("", response_model=schemas.EmployeeResponse)
def add_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return employees_controller.add_employee(employee, db)

@router.get("", response_model=List[schemas.EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    return employees_controller.get_employees(db)

@router.get("/{employee_id}", response_model=schemas.EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    return employees_controller.get_employee(employee_id, db)

@router.put("/{employee_id}", response_model=schemas.EmployeeResponse)
def update_employee(employee_id: int, employee_update: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    return employees_controller.update_employee(employee_id, employee_update, db)

@router.post("/{employee_id}/attendance", response_model=schemas.AttendanceResponse)
def mark_attendance(employee_id: int, attendance: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    return employees_controller.mark_attendance(employee_id, attendance, db)

@router.get("/{employee_id}/attendance", response_model=List[schemas.AttendanceResponse])
def get_attendance_history(employee_id: int, db: Session = Depends(get_db)):
    return employees_controller.get_attendance_history(employee_id, db)
