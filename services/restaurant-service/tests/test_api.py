from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.main import app, get_db
from app.db import Base
from app.models import Restaurant, MenuItem

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_restaurants.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_read_restaurants_and_menu():
    db = TestingSessionLocal()
    restaurant = Restaurant(name="Taco House", cuisine="Mexican", city="Metro", is_open=True)
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)

    menu_item = MenuItem(
        restaurant_id=restaurant.id,
        name="Fish Taco",
        description="Crispy fish with slaw",
        price=9.99,
        available=True,
    )
    db.add(menu_item)
    db.commit()
    db.refresh(menu_item)
    db.close()

    response = client.get("/restaurants")
    assert response.status_code == 200
    assert any(r["name"] == "Taco House" for r in response.json())

    response = client.get("/menu")
    assert response.status_code == 200
    assert any(item["name"] == "Fish Taco" for item in response.json())


def test_patch_availability():
    db = TestingSessionLocal()
    restaurant = Restaurant(name="Burger Barn", cuisine="American", city="Metro")
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)

    menu_item = MenuItem(
        restaurant_id=restaurant.id,
        name="Classic Burger",
        description="Beef patty with cheese",
        price=11.5,
        available=True,
    )
    db.add(menu_item)
    db.commit()
    db.refresh(menu_item)
    db.close()

    response = client.patch(
        "/availability",
        json={"menu_item_id": menu_item.id, "available": False},
    )
    assert response.status_code == 200
    assert response.json()["available"] is False
