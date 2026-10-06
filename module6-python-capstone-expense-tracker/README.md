# SpendWise — Python Capstone Project

A portfolio-ready **Expense Tracker web application** built for Module 6: Python Capstone Project.

The application demonstrates a complete Python web workflow: Flask routing, REST API endpoints, SQLite database storage, CRUD operations, validation, error handling, logging, responsive UI, automated tests, documentation and deployment configuration.

## Features

- Add, edit and delete expenses
- SQLite persistent database
- REST API for expense CRUD operations
- Input validation and useful API errors
- Search and category filtering
- Category spending breakdown
- Responsive mobile-friendly UI
- Centralized error handling
- Application logging
- Pytest API tests
- Production-ready Gunicorn command
- Render deployment configuration

## Technology Stack

- Python 3
- Flask
- SQLite
- HTML5 / CSS3 / JavaScript
- REST API
- Pytest
- Gunicorn

## Project Structure

```text
module6-python-capstone-expense-tracker/
├── app.py
├── requirements.txt
├── pytest.ini
├── render.yaml
├── .python-version
├── README.md
├── docs/
│   ├── PROJECT_REPORT.md
│   └── API_DOCUMENTATION.md
├── tests/
│   └── test_app.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
└── data/
    └── .gitkeep
```

## Run Locally

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the app:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Run Tests

```bash
pytest -q
```

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Health check |
| GET | `/api/expenses` | List expenses |
| POST | `/api/expenses` | Create expense |
| PUT | `/api/expenses/<id>` | Update expense |
| DELETE | `/api/expenses/<id>` | Delete expense |

### Example POST body

```json
{
  "title": "Groceries",
  "amount": 850,
  "category": "Food",
  "expense_date": "2026-10-07",
  "notes": "Weekly groceries"
}
```

## Deployment

The project includes `render.yaml` and a Gunicorn start command for deployment on Render.

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
gunicorn app:app
```

### Important SQLite note

SQLite is ideal for this educational capstone, but the default filesystem on a free cloud web service is not a production-grade persistent database. For a real production system, move the database to PostgreSQL or another managed database.

## Module 6 Requirement Mapping

| Requirement | Implementation |
|---|---|
| Portfolio-ready Python application | SpendWise Expense Tracker |
| Clean file structure | Separate app, templates, static, tests and docs |
| Exception safety | Validation + 404/500 handlers |
| Logging | Python logging configuration |
| System architecture documentation | `docs/PROJECT_REPORT.md` |
| Setup instructions | README |
| Database schema | SQLite `expenses` table |
| Repository | GitHub-ready project |
| Demo video | Record after deployment |
| Deployment | Render configuration |

## Author

Abhay Pratap Mall  
B.Tech CSE Student

This project was created as a learning-focused Python capstone.
