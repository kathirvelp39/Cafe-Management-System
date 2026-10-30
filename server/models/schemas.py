from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Customer Schemas
class CustomerBase(BaseModel):
    email: EmailStr
    full_name: str
    role: str = "admin"

class CustomerCreate(CustomerBase):
    password: str

class CustomerResponse(CustomerBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class PasswordReset(BaseModel):
    email: EmailStr
    new_password: str

class OTPRequest(BaseModel):
    email: EmailStr

class OTPVerify(BaseModel):
    email: EmailStr
    otp_code: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Order Item Schemas
class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = Field(default=1, gt=0)

class OrderItemResponse(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True

# Order Schemas
class OrderBase(BaseModel):
    order_type: str = Field(..., description="dine-in, takeaway, or online")
    table_number: Optional[int] = None
    status: Optional[str] = "Pending"

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderResponse(OrderBase):
    id: int
    customer_id: int
    total_amount: float
    created_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True

# Loyalty Points Schemas
class LoyaltyPointBase(BaseModel):
    points: int
    description: Optional[str] = None

class LoyaltyPointCreate(LoyaltyPointBase):
    pass

class LoyaltyPointResponse(LoyaltyPointBase):
    id: int
    customer_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Feedback Schemas
class FeedbackBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackResponse(FeedbackBase):
    id: int
    customer_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Menu Schemas
class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    price: float = Field(..., gt=0)
    is_available: bool = True

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    is_available: Optional[bool] = None

class MenuItemResponse(MenuItemBase):
    id: int
    image_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Billing and Invoice Schemas
class InvoiceBase(BaseModel):
    order_id: int
    subtotal: float
    tax_amount: float
    total_amount: float
    payment_method: Optional[str] = None
    payment_status: str

class InvoiceResponse(InvoiceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PaymentRequest(BaseModel):
    payment_method: str = Field(..., description="Cash, UPI, or Card")

# Inventory Schemas
class SupplierBase(BaseModel):
    name: str
    contact_person: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class SupplierResponse(SupplierBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class IngredientBase(BaseModel):
    name: str
    unit: str
    minimum_stock_level: float = Field(default=10.0)
    supplier_id: Optional[int] = None

class IngredientCreate(IngredientBase):
    stock_level: float = Field(default=0.0)

class IngredientResponse(IngredientBase):
    id: int
    stock_level: float
    created_at: datetime

    class Config:
        from_attributes = True

class StockTransactionCreate(BaseModel):
    transaction_type: str = Field(..., description="IN or OUT")
    quantity: float = Field(..., gt=0)
    remarks: Optional[str] = None

class StockTransactionResponse(StockTransactionCreate):
    id: int
    ingredient_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Employee and HR Schemas
class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    role: str
    salary: float = Field(default=0.0, ge=0)

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    role: Optional[str] = None
    salary: Optional[float] = Field(None, ge=0)
    is_active: Optional[bool] = None

class EmployeeResponse(EmployeeBase):
    id: int
    hire_date: datetime
    is_active: bool

    class Config:
        from_attributes = True

class AttendanceBase(BaseModel):
    status: str = Field(..., description="Present, Absent, Half-Day, or Leave")

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceResponse(AttendanceBase):
    id: int
    employee_id: int
    date: datetime

    class Config:
        from_attributes = True

# Reports & Analytics Schemas
class SalesSummary(BaseModel):
    period: str
    total_orders: int
    total_revenue: float
    average_order_value: float

class TopItem(BaseModel):
    menu_item_id: int
    name: str
    total_quantity_sold: int

class RevenueAnalytics(BaseModel):
    payment_method: str
    total_revenue: float

class InventoryConsumption(BaseModel):
    ingredient_id: int
    name: str
    total_consumed: float
    unit: str

class CustomerActivity(BaseModel):
    customer_id: int
    full_name: str
    total_orders: int
    total_spent: float

# Reservation Schemas
class TableBase(BaseModel):
    table_number: str
    capacity: int = Field(..., gt=0)

class TableCreate(TableBase):
    pass

class TableResponse(TableBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class ReservationBase(BaseModel):
    customer_id: int
    table_id: int
    reservation_time: datetime
    number_of_guests: int = Field(..., gt=0)

class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(BaseModel):
    status: str = Field(..., description="Pending, Approved, Cancelled, Completed")

class ReservationResponse(ReservationBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# Feedback & Review Schemas
class FeedbackBase(BaseModel):
    customer_id: int
    order_id: Optional[int] = None
    rating: int = Field(..., ge=1, le=5)
    comments: Optional[str] = None
    is_complaint: bool = False

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackUpdate(BaseModel):
    status: str = Field(..., description="Pending, Investigating, Resolved")
    resolution_notes: str

class FeedbackResponse(FeedbackBase):
    id: int
    status: str
    resolution_notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
