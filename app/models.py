from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, constr

class BusinessBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str
    description: Optional[str] = None
    category: str
    is_active: bool = True

class BusinessCreate(BusinessBase):
    password: constr(min_length=8)

class Business(BusinessBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: constr(min_length=8)

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True
