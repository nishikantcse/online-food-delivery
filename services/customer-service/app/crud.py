from sqlalchemy.orm import Session

from . import models, schemas


def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()


def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def create_address(db: Session, address: schemas.AddressCreate, customer_id: int):
    db_address = models.Address(customer_id=customer_id, **address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address
