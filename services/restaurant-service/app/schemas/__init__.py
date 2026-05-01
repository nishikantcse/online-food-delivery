from typing import List, Optional

from pydantic import BaseModel


class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    available: Optional[bool] = True


class MenuItemCreate(MenuItemBase):
    restaurant_id: int


class MenuItem(MenuItemBase):
    id: int
    restaurant_id: int

    class Config:
        orm_mode = True


class RestaurantBase(BaseModel):
    name: str
    cuisine: Optional[str] = None
    city: Optional[str] = None
    is_open: Optional[bool] = True


class RestaurantCreate(RestaurantBase):
    pass


class Restaurant(RestaurantBase):
    id: int
    menu_items: List[MenuItem] = []

    class Config:
        orm_mode = True


class AvailabilityUpdate(BaseModel):
    menu_item_id: int
    available: bool
