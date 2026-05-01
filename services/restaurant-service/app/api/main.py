from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.db import SessionLocal, init_db
from app.models import Restaurant, MenuItem
from app.schemas import (
    AvailabilityUpdate,
    MenuItem as MenuItemSchema,
    Restaurant as RestaurantSchema,
)

init_db()

app = FastAPI(title="Restaurant Service")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/restaurants", response_model=list[RestaurantSchema])
def read_restaurants(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_restaurants(db=db, skip=skip, limit=limit)


@app.get("/menu", response_model=list[MenuItemSchema])
def read_menu(
    restaurant_id: int | None = Query(None, description="Filter menu by restaurant ID"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_menu(db=db, restaurant_id=restaurant_id, skip=skip, limit=limit)


@app.patch("/availability", response_model=MenuItemSchema)
def update_availability(
    payload: AvailabilityUpdate,
    db: Session = Depends(get_db),
):
    menu_item = crud.update_menu_item_availability(
        db=db,
        menu_item_id=payload.menu_item_id,
        available=payload.available,
    )
    if menu_item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return menu_item
