from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = Field(..., ge=1, le=5)
    unit_price: Optional[Decimal] = None


class OrderCreate(BaseModel):
    restaurant_id: int
    items: List[OrderItemCreate]


class OrderItemRead(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    unit_price: Decimal
    total_price: Decimal

    class Config:
        orm_mode = True


class OrderRead(BaseModel):
    id: int
    restaurant_id: int
    total_amount: Decimal
    status: str
    items: List[OrderItemRead]

    class Config:
        orm_mode = True
