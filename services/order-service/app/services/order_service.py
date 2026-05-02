from decimal import Decimal
from typing import Iterable

from fastapi import HTTPException

from app.schemas import OrderCreate
from app.services.restaurant_gateway import RestaurantGateway

MAX_ITEMS = 20
MAX_QUANTITY = 5


def validate_order_payload(order_in: OrderCreate) -> None:
    if len(order_in.items) == 0:
        raise HTTPException(status_code=422, detail="Order must contain at least one item")

    if len(order_in.items) > MAX_ITEMS:
        raise HTTPException(status_code=422, detail=f"Order cannot contain more than {MAX_ITEMS} items")

    for item in order_in.items:
        if item.quantity > MAX_QUANTITY:
            raise HTTPException(
                status_code=422,
                detail=f"Quantity for item {item.menu_item_id} cannot exceed {MAX_QUANTITY}",
            )


def validate_restaurant_and_menu(order_in: OrderCreate) -> None:
    restaurant = RestaurantGateway.get_restaurant(order_in.restaurant_id)
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    if not restaurant.get("is_open", False):
        raise HTTPException(status_code=400, detail="Restaurant is currently closed")

    menu_ids = [item.menu_item_id for item in order_in.items]
    menu_items = list(filter(None, (RestaurantGateway.get_menu_item(menu_id) for menu_id in menu_ids)))
    if len(menu_items) != len(menu_ids):
        missing = set(menu_ids) - {item["id"] for item in menu_items}
        raise HTTPException(status_code=404, detail=f"Menu items not found: {sorted(missing)}")

    unavailable = [item["id"] for item in menu_items if not item.get("available", False)]
    if unavailable:
        raise HTTPException(status_code=400, detail=f"Menu items not available: {sorted(unavailable)}")


def enrich_order_prices(order_in: OrderCreate) -> OrderCreate:
    enriched_items = []
    for item in order_in.items:
        menu_item = RestaurantGateway.get_menu_item(item.menu_item_id)
        if menu_item is None:
            raise HTTPException(status_code=404, detail=f"Menu item {item.menu_item_id} not found")
        enriched_items.append(
            item.copy(update={"unit_price": Decimal(str(menu_item.get("price", 0)))})
        )
    return order_in.copy(update={"items": enriched_items})
