import logging
import os
import sqlite3
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.getenv("DATABASE_PATH", BASE_DIR / "data" / "expenses.db"))

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("expense-tracker")


def get_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                category TEXT NOT NULL,
                expense_date TEXT NOT NULL,
                notes TEXT DEFAULT '',
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def validate_expense(payload):
    if not isinstance(payload, dict):
        return None, "Request body must be a JSON object."

    title = str(payload.get("title", "")).strip()
    category = str(payload.get("category", "")).strip()
    notes = str(payload.get("notes", "")).strip()
    expense_date = str(payload.get("expense_date", "")).strip()

    try:
        amount = float(payload.get("amount"))
    except (TypeError, ValueError):
        return None, "Amount must be a valid number."

    if not title or len(title) > 100:
        return None, "Title is required and must be at most 100 characters."
    if amount <= 0:
        return None, "Amount must be greater than 0."
    if not category or len(category) > 40:
        return None, "Category is required and must be at most 40 characters."
    if not expense_date:
        expense_date = datetime.now().strftime("%Y-%m-%d")
    try:
        datetime.strptime(expense_date, "%Y-%m-%d")
    except ValueError:
        return None, "Expense date must use YYYY-MM-DD format."

    return {
        "title": title,
        "amount": round(amount, 2),
        "category": category,
        "expense_date": expense_date,
        "notes": notes[:500],
    }, None


@app.route("/")
def index():
    return render_template("index.html")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "expense-tracker"})


@app.get("/api/expenses")
def list_expenses():
    category = request.args.get("category", "").strip()
    search = request.args.get("search", "").strip()

    query = "SELECT * FROM expenses WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)
    if search:
        query += " AND (title LIKE ? OR notes LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term])

    query += " ORDER BY expense_date DESC, id DESC"

    with get_db() as conn:
        rows = conn.execute(query, params).fetchall()

    return jsonify([dict(row) for row in rows])


@app.post("/api/expenses")
def create_expense():
    data, error = validate_expense(request.get_json(silent=True))
    if error:
        return jsonify({"error": error}), 400

    with get_db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO expenses
            (title, amount, category, expense_date, notes, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                data["title"],
                data["amount"],
                data["category"],
                data["expense_date"],
                data["notes"],
                datetime.now().isoformat(timespec="seconds"),
            ),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM expenses WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()

    return jsonify(dict(row)), 201


@app.put("/api/expenses/<int:expense_id>")
def update_expense(expense_id):
    data, error = validate_expense(request.get_json(silent=True))
    if error:
        return jsonify({"error": error}), 400

    with get_db() as conn:
        existing = conn.execute(
            "SELECT id FROM expenses WHERE id = ?", (expense_id,)
        ).fetchone()
        if existing is None:
            return jsonify({"error": "Expense not found."}), 404

        conn.execute(
            """
            UPDATE expenses
            SET title = ?, amount = ?, category = ?, expense_date = ?, notes = ?
            WHERE id = ?
            """,
            (
                data["title"],
                data["amount"],
                data["category"],
                data["expense_date"],
                data["notes"],
                expense_id,
            ),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM expenses WHERE id = ?", (expense_id,)
        ).fetchone()

    return jsonify(dict(row))


@app.delete("/api/expenses/<int:expense_id>")
def delete_expense(expense_id):
    with get_db() as conn:
        cursor = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()

    if cursor.rowcount == 0:
        return jsonify({"error": "Expense not found."}), 404

    return jsonify({"message": "Expense deleted successfully."})


@app.errorhandler(404)
def not_found(error):
    if request.path.startswith("/api/"):
        return jsonify({"error": "API endpoint not found."}), 404
    return error


@app.errorhandler(500)
def server_error(error):
    logger.exception("Unhandled server error")
    return jsonify({"error": "Internal server error."}), 500


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
