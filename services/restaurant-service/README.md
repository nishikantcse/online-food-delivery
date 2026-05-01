# Restaurant Service

FastAPI microservice for restaurant management.

## Structure

- `app/api`
- `app/models`
- `app/services`
- `app/repositories`
- `app/schemas`
- `migrations`
- `tests`

## API Endpoints

- `GET /restaurants` - list all restaurants
- `GET /menu` - list all menu items, optionally filtered by `restaurant_id`
- `PATCH /availability` - update a menu item's availability

## Run

```bash
uvicorn app.api.main:app --reload
```
