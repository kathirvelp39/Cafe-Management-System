from sqlalchemy.orm import Session
from server.models import schemas
from server.services import employees_service

def add_employee(employee: schemas.EmployeeCreate, db: Session):
    return employees_service.add_employee(employee, db)

def get_employees(db: Session):
    return employees_service.get_employees(db)

def get_employee(employee_id: int, db: Session):
    return employees_service.get_employee(employee_id, db)

def update_employee(employee_id: int, employee_update: schemas.EmployeeUpdate, db: Session):
    return employees_service.update_employee(employee_id, employee_update, db)

def mark_attendance(employee_id: int, attendance: schemas.AttendanceCreate, db: Session):
    return employees_service.mark_attendance(employee_id, attendance, db)

def get_attendance_history(employee_id: int, db: Session):
    return employees_service.get_attendance_history(employee_id, db)
