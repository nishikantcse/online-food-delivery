from sqlalchemy.orm import Session

from app.models import Order, OrderItem
from app.schemas import OrderCreate


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Order).offset(skip).limit(limit).all()


def create_order(db: Session, order_in: OrderCreate):
    db_order = Order(
        restaurant_id=order_in.restaurant_id,
        total_amount=sum(item.quantity * item.unit_price for item in order_in.items),
        status="confirmed",
    )
    db.add(db_order)
    db.flush()

    for item in order_in.items:
        db_item = OrderItem(
            order_id=db_order.id,
            menu_item_id=item.menu_item_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            total_price=item.quantity * item.unit_price,
        )
        db.add(db_item)

    db.commit()
    db.refresh(db_order)
    return db_order
