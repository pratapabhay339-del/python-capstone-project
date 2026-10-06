# SpendWise — Python Capstone Project Report

## 1. Project Title

**SpendWise — Personal Expense Tracker**

## 2. Project Overview

SpendWise is a full-stack Python web application that helps users record, manage and review personal expenses. It was designed as a portfolio-ready capstone project and demonstrates how Python can be used beyond small scripts to build a complete web application.

The application uses Flask as the backend framework, SQLite for database storage and a responsive HTML/CSS/JavaScript interface for the user experience.

## 3. Problem Statement

Students and young professionals often record expenses informally or do not track them at all. This makes it difficult to understand where money is being spent.

SpendWise provides a simple interface to record expenses, edit incorrect entries, remove transactions, search records and view spending by category.

## 4. Objectives

- Build a complete Python web application.
- Apply Flask routing and request handling.
- Implement REST API endpoints.
- Store data using SQLite.
- Implement CRUD operations.
- Validate user input.
- Handle common application errors safely.
- Add application logging.
- Create automated endpoint tests.
- Document architecture, setup and database design.
- Prepare the application for cloud deployment.

## 5. Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python + Flask |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| API | REST/JSON |
| Testing | Pytest |
| Production server | Gunicorn |
| Deployment target | Render |

## 6. System Architecture

```text
                 ┌────────────────────────┐
                 │      User Browser      │
                 │ HTML / CSS / JavaScript│
                 └────────────┬───────────┘
                              │ HTTP / JSON
                              ▼
                 ┌────────────────────────┐
                 │      Flask Server      │
                 │ Routes + Validation    │
                 │ Error Handling + Logs  │
                 └────────────┬───────────┘
                              │ SQL
                              ▼
                 ┌────────────────────────┐
                 │       SQLite DB        │
                 │       expenses         │
                 └────────────────────────┘
```

## 7. Main Components

### Flask Application

`app.py` contains the web routes, REST API routes, database helper functions, validation logic and error handlers.

### Frontend

The interface is split into:

- `templates/index.html`
- `static/style.css`
- `static/app.js`

The browser communicates with Flask through JSON API requests.

### Database

SQLite stores expense records locally in:

```text
data/expenses.db
```

The database is created automatically when the application starts.

## 8. Database Schema

### expenses

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| title | TEXT | Expense title |
| amount | REAL | Positive expense amount |
| category | TEXT | Spending category |
| expense_date | TEXT | Date in YYYY-MM-DD format |
| notes | TEXT | Optional notes |
| created_at | TEXT | Creation timestamp |

## 9. CRUD Operations

### Create

`POST /api/expenses`

Creates a new expense after validating the request.

### Read

`GET /api/expenses`

Returns stored expenses. Optional category and search filters are supported.

### Update

`PUT /api/expenses/<id>`

Updates an existing expense.

### Delete

`DELETE /api/expenses/<id>`

Deletes an expense by ID.

## 10. Validation

The backend validates:

- Required title
- Positive numeric amount
- Required category
- Valid date format
- Maximum title length
- Maximum notes length

Invalid requests return HTTP 400 with a JSON error message.

## 11. Exception Safety and Logging

The application includes:

- API-specific 404 responses
- Global 500 error handling
- Python logging for unexpected server errors
- Validation before database writes
- Database context management

This prevents many common errors from producing unclear responses to users.

## 12. Testing

Pytest tests cover:

- Health endpoint
- Expense creation
- Expense listing
- Expense update
- Expense deletion
- Validation of invalid amounts

Run:

```bash
pytest -q
```

## 13. User Workflow

```text
Open application
       ↓
Add expense
       ↓
Validate input
       ↓
Store in SQLite
       ↓
Refresh expense list
       ↓
Search / filter / edit / delete
       ↓
View category breakdown
```

## 14. Deployment Plan

The application can be deployed as a Flask web service.

Production start command:

```bash
gunicorn app:app
```

The included `render.yaml` provides deployment configuration.

## 15. Future Improvements

- User login and registration
- JWT authentication
- PostgreSQL database
- Monthly budget limits
- CSV/PDF export
- Income tracking
- Monthly reports
- Interactive charts
- Email notifications
- Cloud database backups

## 16. Learning Outcomes

Through this project I practiced:

- Flask application development
- REST API design
- SQLite database integration
- SQL CRUD operations
- Request validation
- Error handling
- Logging
- Automated testing
- Frontend/backend integration
- Project documentation
- Deployment preparation

## 17. Conclusion

SpendWise demonstrates a complete Python application workflow from user interface to backend API and database storage. It combines the concepts learned during the earlier Python modules into one practical capstone project suitable for a student portfolio.
