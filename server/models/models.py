from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from server.config.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(50), nullable=False, default="admin")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    otp_code = Column(String(10), nullable=True)
    otp_expiry = Column(DateTime(timezone=True), nullable=True)

    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")
    loyalty_points = relationship("LoyaltyPoint", back_populates="customer", cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="customer", cascade="all, delete-orphan")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    order_type = Column(String(50), nullable=False) # e.g., dine-in, takeaway, online
    table_number = Column(Integer, nullable=True) # only for dine-in
    total_amount = Column(Float, nullable=False, default=0.0)
    status = Column(String(50), default="Pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem")

class LoyaltyPoint(Base):
    __tablename__ = "loyalty_points"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    points = Column(Integer, nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    customer = relationship("Customer", back_populates="loyalty_points")



class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    category = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True)
    subtotal = Column(Float, nullable=False)
    tax_amount = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=True) # Cash, UPI, Card
    payment_status = Column(String(50), default="Pending") # Pending, Paid
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    order = relationship("Order")

class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    contact_person = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    address = Column(String(1000), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Ingredient(Base):
    __tablename__ = "ingredients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    unit = Column(String(50), nullable=False) # e.g., kg, L, units
    stock_level = Column(Float, nullable=False, default=0.0)
    minimum_stock_level = Column(Float, nullable=False, default=10.0)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    supplier = relationship("Supplier")
    transactions = relationship("StockTransaction", back_populates="ingredient")

class StockTransaction(Base):
    __tablename__ = "stock_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))
    transaction_type = Column(String(10), nullable=False) # IN or OUT
    quantity = Column(Float, nullable=False)
    remarks = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    ingredient = relationship("Ingredient", back_populates="transactions")

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(50), nullable=True)
    role = Column(String(100), nullable=False)
    salary = Column(Float, nullable=False, default=0.0)
    hire_date = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    attendance = relationship("Attendance", back_populates="employee", cascade="all, delete-orphan")

class Attendance(Base):
    __tablename__ = "attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), nullable=False) # Present, Absent, Half-Day, Leave
    
    employee = relationship("Employee", back_populates="attendance")

class RestaurantTable(Base):
    __tablename__ = "tables"
    
    id = Column(Integer, primary_key=True, index=True)
    table_number = Column(String(50), unique=True, index=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)

class Reservation(Base):
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False)
    reservation_time = Column(DateTime(timezone=True), nullable=False)
    number_of_guests = Column(Integer, nullable=False)
    status = Column(String(50), default="Pending") # Pending, Approved, Cancelled, Completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    customer = relationship("Customer")
    table = relationship("RestaurantTable")

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    rating = Column(Integer, nullable=False) # 1 to 5
    comments = Column(String(2000), nullable=True)
    is_complaint = Column(Boolean, default=False)
    status = Column(String(50), default="Pending") # Pending, Investigating, Resolved
    resolution_notes = Column(String(2000), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    customer = relationship("Customer", back_populates="feedback")
    order = relationship("Order")
