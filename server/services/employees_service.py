from sqlalchemy.orm import Session
from fastapi import HTTPException
from server.models import models, schemas

def add_employee(employee: schemas.EmployeeCreate, db: Session):
    existing_emp = db.query(models.Employee).filter(models.Employee.email == employee.email).first()
    if existing_emp:
        raise HTTPException(status_code=400, detail="Email already registered for another employee")
        
    new_employee = models.Employee(**employee.model_dump())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    
    # Send welcome email and SMS
    if new_employee.email:
        from server.services.email_service import send_email
        subject = f"Welcome to the team, {new_employee.full_name}!"
        body = f"Hi {new_employee.full_name},\n\nWelcome to Monika G Cafe! We are thrilled to have you join us as a {new_employee.role}.\n\nYour starting salary is recorded as ${new_employee.salary:.2f}.\n\nBest regards,\nMonika G Cafe Management"
        # We don't block the API response if the email fails, so we catch potential errors
        try:
            send_email(to_email=new_employee.email, subject=subject, body=body)
        except Exception as e:
            print(f"Could not send welcome email to {new_employee.email}: {e}")
            
    if new_employee.phone:
        from server.services.sms_service import send_sms
        sms_msg = f"Hi {new_employee.full_name}, welcome to the team at Monika G Cafe! We're excited to have you as our newest {new_employee.role}."
        try:
            send_sms(to_phone=new_employee.phone, message=sms_msg)
        except Exception as e:
            print(f"Could not send welcome SMS to {new_employee.phone}: {e}")
            
    return new_employee

def get_employees(db: Session):
    return db.query(models.Employee).all()

def get_employee(employee_id: int, db: Session):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

def update_employee(employee_id: int, employee_update: schemas.EmployeeUpdate, db: Session):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
        
    update_data = employee_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(employee, key, value)
        
    db.commit()
    db.refresh(employee)
    return employee

def mark_attendance(employee_id: int, attendance: schemas.AttendanceCreate, db: Session):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
        
    if not employee.is_active:
        raise HTTPException(status_code=400, detail="Cannot mark attendance for an inactive employee")
        
    valid_statuses = ["Present", "Absent", "Half-Day", "Leave"]
    if attendance.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of {valid_statuses}")
        
    new_attendance = models.Attendance(**attendance.model_dump(), employee_id=employee_id)
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    return new_attendance

def get_attendance_history(employee_id: int, db: Session):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
        
    return db.query(models.Attendance).filter(models.Attendance.employee_id == employee_id).all()
