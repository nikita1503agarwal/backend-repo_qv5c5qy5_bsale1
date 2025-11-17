"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Papayow order schema
class Order(BaseModel):
    """
    Orders placed from the Papayow single-page site
    Collection name: "order"
    """
    parent_email: EmailStr = Field(..., description="Parent contact email")
    description: Optional[str] = Field(None, description="Short notes or preferences")
    product_type: Literal['figurine', 'coloring_book'] = Field(..., description="Requested product")
    photo_filename: Optional[str] = Field(None, description="Stored filename of uploaded photo")
    status: Literal['received', 'processing', 'completed'] = Field('received', description="Order status")
