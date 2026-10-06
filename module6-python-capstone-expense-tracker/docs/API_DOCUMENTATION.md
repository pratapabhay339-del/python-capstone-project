# SpendWise API Documentation

Base URL (local):

```text
http://127.0.0.1:5000
```

## Health

### GET `/api/health`

Response:

```json
{
  "status": "ok",
  "service": "expense-tracker"
}
```

## List Expenses

### GET `/api/expenses`

Optional query parameters:

- `category`
- `search`

Example:

```text
/api/expenses?category=Food
```

## Create Expense

### POST `/api/expenses`

Request:

```json
{
  "title": "Books",
  "amount": 799,
  "category": "Education",
  "expense_date": "2026-10-07",
  "notes": "Python reference book"
}
```

Success: `201 Created`

## Update Expense

### PUT `/api/expenses/{id}`

Uses the same JSON structure as create.

Success: `200 OK`

## Delete Expense

### DELETE `/api/expenses/{id}`

Success:

```json
{
  "message": "Expense deleted successfully."
}
```

## Error Format

Validation errors use:

```json
{
  "error": "Amount must be greater than 0."
}
```

Common status codes:

- `200` Success
- `201` Created
- `400` Invalid input
- `404` Resource/endpoint not found
- `500` Internal server error
