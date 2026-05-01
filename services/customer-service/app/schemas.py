from typing import List, Optional

from pydantic import BaseModel, EmailStr


class AddressBase(BaseModel):
    street: str
    city: str
    state: Optional[str] = None
    zip_code: Optional[str] = None


class AddressCreate(AddressBase):
    pass


class Address(AddressBase):
    id: int
    customer_id: int

    class Config:
        orm_mode = True


class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int
    addresses: List[Address] = []

    class Config:
        orm_mode = True
