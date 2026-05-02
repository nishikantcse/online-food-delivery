from decimal import Decimal

from fastapi.testclient import TestClient

from app.api.main import app
from app.services.restaurant_gateway import RestaurantGateway

client = TestClient(app)


def test_create_order_success(monkeypatch):
    monkeypatch.setattr(
        RestaurantGateway,
        "get_restaurant",
        staticmethod(lambda restaurant_id: {"id": restaurant_id, "is_open": True}),
    )
    monkeypatch.setattr(
        RestaurantGateway,
        "get_menu_item",
        staticmethod(lambda menu_item_id: {"id": menu_item_id, "available": True, "price": 10.0}),
    )

    response = client.post(
        "/orders",
        json={
            "restaurant_id": 1,
            "items": [
                {"menu_item_id": 101, "quantity": 2},
                {"menu_item_id": 102, "quantity": 1},
            ],
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["restaurant_id"] == 1
    assert payload["total_amount"] == "30.00"
    assert len(payload["items"]) == 2


def test_order_rejects_closed_restaurant(monkeypatch):
    monkeypatch.setattr(
        RestaurantGateway,
        "get_restaurant",
        staticmethod(lambda restaurant_id: {"id": restaurant_id, "is_open": False}),
    )
    monkeypatch.setattr(
        RestaurantGateway,
        "get_menu_item",
        staticmethod(lambda menu_item_id: {"id": menu_item_id, "available": True, "price": 5.0}),
    )

    response = client.post(
        "/orders",
        json={
            "restaurant_id": 2,
            "items": [{"menu_item_id": 200, "quantity": 1}],
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Restaurant is currently closed"


def test_order_rejects_unavailable_item(monkeypatch):
    monkeypatch.setattr(
        RestaurantGateway,
        "get_restaurant",
        staticmethod(lambda restaurant_id: {"id": restaurant_id, "is_open": True}),
    )
    monkeypatch.setattr(
        RestaurantGateway,
        "get_menu_item",
        staticmethod(lambda menu_item_id: {"id": menu_item_id, "available": False, "price": 5.0}),
    )

    response = client.post(
        "/orders",
        json={
            "restaurant_id": 3,
            "items": [{"menu_item_id": 300, "quantity": 1}],
        },
    )

    assert response.status_code == 400
    assert "Menu items not available" in response.json()["detail"]


def test_order_rejects_large_quantity(monkeypatch):
    monkeypatch.setattr(
        RestaurantGateway,
        "get_restaurant",
        staticmethod(lambda restaurant_id: {"id": restaurant_id, "is_open": True}),
    )
    monkeypatch.setattr(
        RestaurantGateway,
        "get_menu_item",
        staticmethod(lambda menu_item_id: {"id": menu_item_id, "available": True, "price": 8.0}),
    )

    response = client.post(
        "/orders",
        json={
            "restaurant_id": 4,
            "items": [{"menu_item_id": 400, "quantity": 6}],
        },
    )

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any("less than or equal to 5" in err.get("msg", "") for err in detail)
