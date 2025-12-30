from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Client(Base):
    """Cliente - Customer model"""
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, index=True, nullable=False)  # Multi-tenancy
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    address = Column(Text)
    document = Column(String)  # CPF/CNPJ
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sales = relationship("Sale", back_populates="client")


class Product(Base):
    """Produto - Product/Service model"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, index=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    sku = Column(String, unique=True, index=True)
    category = Column(String)
    unit_price = Column(Float, nullable=False)
    cost_price = Column(Float, nullable=False)
    margin = Column(Float)  # Calculated: (unit_price - cost_price) / cost_price
    stock_quantity = Column(Integer, default=0)
    min_stock = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    inventory_entries = relationship("InventoryEntry", back_populates="product")
    sale_items = relationship("SaleItem", back_populates="product")


class Seller(Base):
    """Vendedor - Seller/Salesperson model"""
    __tablename__ = "sellers"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, index=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    commission_rate = Column(Float, default=0.0)  # Percentage
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sales = relationship("Sale", back_populates="seller")


class Sale(Base):
    """Venda - Sale model"""
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, index=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=True)
    sale_date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)
    final_amount = Column(Float, nullable=False)
    payment_method = Column(String)  # cash, credit, debit, pix
    status = Column(String, default="completed")  # completed, cancelled, pending
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = relationship("Client", back_populates="sales")
    seller = relationship("Seller", back_populates="sales")
    items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")


class SaleItem(Base):
    """Item de Venda - Sale line item"""
    __tablename__ = "sale_items"
    
    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    
    # Relationships
    sale = relationship("Sale", back_populates="items")
    product = relationship("Product", back_populates="sale_items")


class InventoryEntry(Base):
    """Entrada de Estoque - Inventory entry/movement"""
    __tablename__ = "inventory_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, index=True, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    entry_type = Column(String, nullable=False)  # purchase, adjustment, return
    quantity = Column(Integer, nullable=False)
    unit_cost = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)
    entry_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="inventory_entries")


class Cost(Base):
    """Custo - Operational cost model"""
    __tablename__ = "costs"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, index=True, nullable=False)
    category = Column(String, nullable=False)  # rent, utilities, salaries, etc.
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    cost_date = Column(DateTime, default=datetime.utcnow)
    is_recurring = Column(Integer, default=0)  # 0=one-time, 1=monthly
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
