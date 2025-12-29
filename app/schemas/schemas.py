from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# Client Schemas
class ClientBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    document: Optional[str] = None


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    document: Optional[str] = None


class Client(ClientBase):
    id: int
    client_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Product Schemas
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    sku: Optional[str] = None
    category: Optional[str] = None
    unit_price: float
    cost_price: float
    stock_quantity: Optional[int] = 0
    min_stock: Optional[int] = 0


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    unit_price: Optional[float] = None
    cost_price: Optional[float] = None
    stock_quantity: Optional[int] = None
    min_stock: Optional[int] = None


class Product(ProductBase):
    id: int
    client_id: str
    margin: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Seller Schemas
class SellerBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    commission_rate: Optional[float] = 0.0


class SellerCreate(SellerBase):
    pass


class SellerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    commission_rate: Optional[float] = None


class Seller(SellerBase):
    id: int
    client_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Sale Item Schema
class SaleItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float


class SaleItemCreate(SaleItemBase):
    pass


class SaleItem(SaleItemBase):
    id: int
    sale_id: int
    subtotal: float
    
    class Config:
        from_attributes = True


# Sale Schemas
class SaleBase(BaseModel):
    customer_id: int
    seller_id: Optional[int] = None
    discount: Optional[float] = 0.0
    payment_method: Optional[str] = None
    status: Optional[str] = "completed"
    notes: Optional[str] = None


class SaleCreate(SaleBase):
    items: list[SaleItemCreate]


class Sale(SaleBase):
    id: int
    client_id: str
    sale_date: datetime
    total_amount: float
    final_amount: float
    created_at: datetime
    updated_at: datetime
    items: list[SaleItem] = []
    
    class Config:
        from_attributes = True


# Inventory Entry Schemas
class InventoryEntryBase(BaseModel):
    product_id: int
    entry_type: str
    quantity: int
    unit_cost: float
    notes: Optional[str] = None


class InventoryEntryCreate(InventoryEntryBase):
    pass


class InventoryEntry(InventoryEntryBase):
    id: int
    client_id: str
    total_cost: float
    entry_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


# Cost Schemas
class CostBase(BaseModel):
    category: str
    description: str
    amount: float
    is_recurring: Optional[int] = 0
    notes: Optional[str] = None


class CostCreate(CostBase):
    pass


class CostUpdate(BaseModel):
    category: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    is_recurring: Optional[int] = None
    notes: Optional[str] = None


class Cost(CostBase):
    id: int
    client_id: str
    cost_date: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
