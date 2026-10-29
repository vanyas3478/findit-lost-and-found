"""
Lost & Found Management System
Beginner-friendly DBMS project using Flask and SQLite.
Run with: python app.py
Open: http://127.0.0.1:5000
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "classroom-demo-secret-key"
DATABASE = Path(__file__).parent / "lost_found.db"

CATEGORIES = ["ID Card", "Electronics", "Wallet", "Books", "Keys", "Clothing", "Bag", "Other"]


# Connect to the SQLite database
def connect_db():
    database = sqlite3.connect(DATABASE)
    database.row_factory = sqlite3.Row
    return database


# Create tables and sample records when the program starts
def setup_database():
    database = connect_db()

    database.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'student'
        )
    """)

    database.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            item_type TEXT NOT NULL,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            location TEXT NOT NULL,
            event_date TEXT NOT NULL,
            contact TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Open',
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    database.execute("""
        CREATE TABLE IF NOT EXISTS claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            FOREIGN KEY (item_id) REFERENCES items(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Add demo accounts only if they do not already exist
    student = database.execute(
        "SELECT id FROM users WHERE email = ?", ("student@demo.com",)
    ).fetchone()

    if student is None:
        database.execute(
            "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
            ("Demo Student", "student@demo.com", "student123", "student")
        )
        student_id = database.execute(
            "SELECT id FROM users WHERE email = ?", ("student@demo.com",)
        ).fetchone()["id"]

        demo_items = [
            (student_id, "Lost", "Blue College ID Card", "ID Card",
             "Blue ID card with a clear plastic holder.", "College Library",
             "2026-10-20", "student@demo.com", "Open"),
            (student_id, "Found", "Black Water Bottle", "Other",
             "Black steel bottle found near the canteen.", "College Canteen",
             "2026-10-22", "student@demo.com", "Open"),
            (student_id, "Lost", "White Earbuds Case", "Electronics",
             "Small white wireless earbuds case.", "Computer Lab",
             "2026-10-23", "student@demo.com", "Open")
        ]
        database.executemany("""
            INSERT INTO items
            (user_id, item_type, title, category, description, location, event_date, contact, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, demo_items)

    admin = database.execute(
        "SELECT id FROM users WHERE email = ?", ("admin@demo.com",)
    ).fetchone()
    if admin is None:
        database.execute(
            "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
            ("Project Admin", "admin@demo.com", "admin123", "admin")
        )

    database.commit()
    database.close()


# Home page: show and search items
@app.route("/")
def home():
    search_text = request.args.get("search", "")
    item_type = request.args.get("type", "")

    database = connect_db()
    sql = "SELECT * FROM items WHERE status != 'Resolved'"
    values = []

    if search_text:
        sql += " AND (title LIKE ? OR description LIKE ? OR location LIKE ?)"
        word = "%" + search_text + "%"
        values.extend([word, word, word])

    if item_type in ["Lost", "Found"]:
        sql += " AND item_type = ?"
        values.append(item_type)

    sql += " ORDER BY id DESC"
    items = database.execute(sql, values).fetchall()

    total = database.execute("SELECT COUNT(*) FROM items WHERE status != 'Resolved'").fetchone()[0]
    lost = database.execute("SELECT COUNT(*) FROM items WHERE item_type='Lost' AND status != 'Resolved'").fetchone()[0]
    found = database.execute("SELECT COUNT(*) FROM items WHERE item_type='Found' AND status != 'Resolved'").fetchone()[0]
    database.close()

    return render_template("home.html", items=items, search_text=search_text,
                           item_type=item_type, total=total, lost=lost, found=found)


# Register a new student account
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        if not name or not email or len(password) < 6:
            flash("Enter your name and email. Password must have at least 6 characters.")
            return redirect(url_for("register"))

        database = connect_db()
        try:
            database.execute(
                "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                (name, email, password, "student")
            )
            database.commit()
            flash("Account created. Please log in.")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("This email is already registered.")
        finally:
            database.close()

    return render_template("register.html")


# Log in
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        database = connect_db()
        user = database.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        ).fetchone()
        database.close()

        if user:
            session["user_id"] = user["id"]
            session["name"] = user["name"]
            session["role"] = user["role"]
            flash("You are logged in.")
            return redirect(url_for("home"))

        flash("Incorrect email or password.")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have logged out.")
    return redirect(url_for("home"))


# Add a lost or found report
@app.route("/report", methods=["GET", "POST"])
def report():
    if "user_id" not in session:
        flash("Please log in before submitting a report.")
        return redirect(url_for("login"))

    if request.method == "POST":
        item_type = request.form["item_type"]
        title = request.form["title"].strip()
        category = request.form["category"]
        description = request.form["description"].strip()
        location = request.form["location"].strip()
        event_date = request.form["event_date"]
        contact = request.form["contact"].strip()

        if not all([title, description, location, event_date, contact]):
            flash("Please fill in all the fields.")
            return redirect(url_for("report"))

        database = connect_db()
        database.execute("""
            INSERT INTO items
            (user_id, item_type, title, category, description, location, event_date, contact)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (session["user_id"], item_type, title, category, description,
              location, event_date, contact))
        database.commit()
        database.close()

        flash("Your item report has been saved.")
        return redirect(url_for("home"))

    return render_template("report.html", categories=CATEGORIES)


# Show full details of one item
@app.route("/item/<int:item_id>")
def item_details(item_id):
    database = connect_db()
    item = database.execute("SELECT * FROM items WHERE id=?", (item_id,)).fetchone()
    database.close()

    if item is None:
        return "Item not found", 404

    return render_template("details.html", item=item)


# Submit an ownership claim
@app.route("/claim/<int:item_id>", methods=["POST"])
def claim(item_id):
    if "user_id" not in session:
        flash("Please log in before making a claim.")
        return redirect(url_for("login"))

    message = request.form["message"].strip()
    if not message:
        flash("Please explain why this item belongs to you.")
        return redirect(url_for("item_details", item_id=item_id))

    database = connect_db()
    item = database.execute("SELECT * FROM items WHERE id=?", (item_id,)).fetchone()

    if item is None:
        database.close()
        return "Item not found", 404

    if item["user_id"] == session["user_id"]:
        database.close()
        flash("You cannot claim your own report.")
        return redirect(url_for("item_details", item_id=item_id))

    database.execute(
        "INSERT INTO claims (item_id, user_id, message) VALUES (?, ?, ?)",
        (item_id, session["user_id"], message)
    )
    database.execute("UPDATE items SET status='Claim Pending' WHERE id=?", (item_id,))
    database.commit()
    database.close()

    flash("Your claim has been submitted.")
    return redirect(url_for("item_details", item_id=item_id))


# Student's own reports
@app.route("/my-reports")
def my_reports():
    if "user_id" not in session:
        flash("Please log in to view your reports.")
        return redirect(url_for("login"))

    database = connect_db()
    items = database.execute(
        "SELECT * FROM items WHERE user_id=? ORDER BY id DESC",
        (session["user_id"],)
    ).fetchall()
    database.close()
    return render_template("my_reports.html", items=items)


# Admin dashboard
@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        flash("Please log in using the admin account.")
        return redirect(url_for("login"))

    database = connect_db()
    items = database.execute("SELECT * FROM items ORDER BY id DESC").fetchall()
    claims = database.execute("""
        SELECT claims.*, items.title, users.name AS claimant_name
        FROM claims
        JOIN items ON claims.item_id = items.id
        JOIN users ON claims.user_id = users.id
        ORDER BY claims.id DESC
    """).fetchall()
    user_count = database.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    database.close()

    return render_template("admin.html", items=items, claims=claims, user_count=user_count)


# Change an item's status (admin only)
@app.route("/admin/status/<int:item_id>", methods=["POST"])
def change_status(item_id):
    if session.get("role") != "admin":
        return "Access denied", 403

    status = request.form["status"]
    if status not in ["Open", "Claim Pending", "Resolved"]:
        return "Invalid status", 400

    database = connect_db()
    database.execute("UPDATE items SET status=? WHERE id=?", (status, item_id))
    database.commit()
    database.close()
    flash("Item status updated.")
    return redirect(url_for("admin"))


# Approve or reject a claim (admin only)
@app.route("/admin/claim/<int:claim_id>", methods=["POST"])
def decide_claim(claim_id):
    if session.get("role") != "admin":
        return "Access denied", 403

    status = request.form["status"]
    if status not in ["Approved", "Rejected"]:
        return "Invalid claim status", 400

    database = connect_db()
    claim_row = database.execute("SELECT item_id FROM claims WHERE id=?", (claim_id,)).fetchone()
    if claim_row is None:
        database.close()
        return "Claim not found", 404

    database.execute("UPDATE claims SET status=? WHERE id=?", (status, claim_id))
    if status == "Approved":
        database.execute("UPDATE items SET status='Resolved' WHERE id=?", (claim_row["item_id"],))
    else:
        database.execute("UPDATE items SET status='Open' WHERE id=? AND status='Claim Pending'", (claim_row["item_id"],))
    database.commit()
    database.close()

    flash("Claim decision saved.")
    return redirect(url_for("admin"))


if __name__ == "__main__":
    setup_database()
    app.run(debug=True)
