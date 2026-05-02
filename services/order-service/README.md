# Order Service

FastAPI microservice for order processing.

## Structure

- `app/api`
- `app/models`
- `app/services`
- `app/repositories`
- `app/schemas`
- `migrations`
- `tests`

## Responsibilities

- Validate restaurant is open before accepting orders
- Validate each menu item is available
- Enforce business rules:
  - max 20 order items
  - quantity per item ≤ 5
- Calculate total order amount

## API Endpoints

- `POST /orders` - create a new order
- `GET /orders` - list orders

## Run

```bash
uvicorn app.api.main:app --reload
```
