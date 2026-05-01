from sqlalchemy.orm import Session

from app.models import MenuItem, Restaurant
from app.schemas import MenuItemCreate


def get_restaurants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Restaurant).offset(skip).limit(limit).all()


def get_menu(db: Session, restaurant_id: int | None = None, skip: int = 0, limit: int = 100):
    query = db.query(MenuItem)
    if restaurant_id is not None:
        query = query.filter(MenuItem.restaurant_id == restaurant_id)
    return query.offset(skip).limit(limit).all()


def create_menu_item(db: Session, menu_item: MenuItemCreate):
    db_item = MenuItem(**menu_item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_menu_item_availability(db: Session, menu_item_id: int, available: bool):
    menu_item = db.get(MenuItem, menu_item_id)
    if menu_item is None:
        return None
    menu_item.available = available
    db.add(menu_item)
    db.commit()
    db.refresh(menu_item)
    return menu_item
