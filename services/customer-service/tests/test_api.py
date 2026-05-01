from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


def test_create_and_get_customers():
    response = client.post(
        "/customers",
        json={
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "phone": "+1234567890",
        },
    )
    assert response.status_code == 201
    created = response.json()
    assert created["email"] == "jane.doe@example.com"

    response = client.get("/customers")
    assert response.status_code == 200
    assert any(customer["email"] == "jane.doe@example.com" for customer in response.json())


def test_create_address_for_customer():
    response = client.post(
        "/customers",
        json={
            "name": "Bob Smith",
            "email": "bob.smith@example.com",
        },
    )
    assert response.status_code == 201
    customer = response.json()

    response = client.post(
        "/addresses?customer_id=%s" % customer["id"],
        json={
            "street": "123 Main St",
            "city": "Metropolis",
            "state": "NY",
            "zip_code": "12345",
        },
    )
    assert response.status_code == 201
    address = response.json()
    assert address["customer_id"] == customer["id"]
    assert address["street"] == "123 Main St"
