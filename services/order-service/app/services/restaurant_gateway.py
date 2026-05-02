import os
from typing import Any

import requests

RESTO_SERVICE_URL = os.getenv("RESTAURANT_SERVICE_URL", "http://localhost:8002")


class RestaurantGateway:
    @staticmethod
    def get_restaurant(restaurant_id: int) -> dict[str, Any] | None:
        try:
            response = requests.get(f"{RESTO_SERVICE_URL}/restaurants")
            response.raise_for_status()
            restaurants = response.json()
            return next((r for r in restaurants if r.get("id") == restaurant_id), None)
        except requests.RequestException:
            return None

    @staticmethod
    def get_menu_item(menu_item_id: int) -> dict[str, Any] | None:
        try:
            response = requests.get(f"{RESTO_SERVICE_URL}/menu")
            response.raise_for_status()
            items = response.json()
            return next((item for item in items if item.get("id") == menu_item_id), None)
        except requests.RequestException:
            return None
