from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.db import SessionLocal, init_db
from app.schemas import OrderCreate, OrderRead
from app.services.order_service import (
    enrich_order_prices,
    validate_order_payload,
    validate_restaurant_and_menu,
)

init_db()

app = FastAPI(title="Order Service")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/orders", response_model=OrderRead, status_code=201)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    validate_order_payload(order)
    validate_restaurant_and_menu(order)
    order_with_prices = enrich_order_prices(order)
    return crud.create_order(db=db, order_in=order_with_prices)


@app.get("/orders", response_model=list[OrderRead])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orders(db=db, skip=skip, limit=limit)
