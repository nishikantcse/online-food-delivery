from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.db import SessionLocal, init_db

init_db()

app = FastAPI(title="Customer Service")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/customers", response_model=schemas.Customer, status_code=201)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Customer).filter(models.Customer.email == customer.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Customer with this email already exists")
    return crud.create_customer(db=db, customer=customer)


@app.get("/customers", response_model=list[schemas.Customer])
def read_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_customers(db=db, skip=skip, limit=limit)


@app.post("/addresses", response_model=schemas.Address, status_code=201)
def create_address(
    address: schemas.AddressCreate,
    customer_id: int = Query(..., description="Customer ID for the new address"),
    db: Session = Depends(get_db),
):
    customer = db.get(models.Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return crud.create_address(db=db, address=address, customer_id=customer_id)
