from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

DATABASE = "database.db"
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------- DATABASE CONNECTION ----------------
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- DATABASE INITIALIZATION ----------------
def init_db():
    conn = get_db()
    cur = conn.cursor()

    # Users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)

    # Complaints table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            category TEXT,
            description TEXT,
            image TEXT,
            status TEXT,
            assigned_to INTEGER,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=? AND role=?",
            (email, password, role.lower())
        ).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["role"] = user["role"]

            if role == "Student":
                return redirect("/student/dashboard")
            elif role == "Admin":
                return redirect("/admin/dashboard")
            elif role == "Technician":
                return redirect("/technician/dashboard")
            elif role == "ICC":
                return redirect("/icc/dashboard")

        return "Invalid credentials"

    return render_template("login_page.html")


# ---------------- STUDENT SIGNUP ----------------
@app.route("/student/signup", methods=["GET", "POST"])
def student_signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        conn.execute(
            "INSERT INTO users (name, email, password, role) VALUES (?,?,?,?)",
            (name, email, password, "student")
        )
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("student_signup.html")


# ---------------- ADMIN SIGNUP ----------------
@app.route("/admin/signup", methods=["GET", "POST"])
def admin_signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        conn.execute(
            "INSERT INTO users (name, email, password, role) VALUES (?,?,?,?)",
            (name, email, password, "admin")
        )
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("admin_signup.html")


# ---------------- STUDENT DASHBOARD ----------------
@app.route("/student/dashboard")
def student_dashboard():
    return render_template("Student_Dashboard.html")


# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("Adminpanel.html")


# ---------------- TECHNICIAN DASHBOARD ----------------
@app.route("/technician/dashboard")
def technician_dashboard():
    return render_template("Technician_Dashboard.html")


# ---------------- ICC DASHBOARD ----------------
@app.route("/icc/dashboard")
def icc_dashboard():
    return "ICC Dashboard (Backend Ready)"


# ---------------- LAB COMPLAINT ----------------
@app.route("/complaint/lab", methods=["GET", "POST"])
def lab_complaint():
    if request.method == "POST":
        lab = request.form.get("lab")
        category = request.form.get("category")
        description = request.form.get("description")

        image = request.files.get("image")
        image_name = None

        if image:
            image_name = image.filename
            image.save(os.path.join(UPLOAD_FOLDER, image_name))

        conn = get_db()
        conn.execute("""
            INSERT INTO complaints
            (user_id, type, category, description, image, status, created_at)
            VALUES (?,?,?,?,?,?,?)
        """, (
            session.get("user_id"),
            "lab",
            category,
            description,
            image_name,
            "Pending",
            datetime.now()
        ))
        conn.commit()
        conn.close()

        return redirect("/complaints/my")

    return render_template("complaint_Form.html")


# ---------------- ICC COMPLAINT ----------------
@app.route("/complaint/icc", methods=["GET", "POST"])
def icc_complaint():
    if request.method == "POST":
        category = request.form.get("category")
        description = request.form.get("description")

        file = request.files.get("evidence")
        file_name = None

        if file:
            file_name = file.filename
            file.save(os.path.join(UPLOAD_FOLDER, file_name))

        conn = get_db()
        conn.execute("""
            INSERT INTO complaints
            (user_id, type, category, description, image, status, created_at)
            VALUES (?,?,?,?,?,?,?)
        """, (
            session.get("user_id"),
            "icc",
            category,
            description,
            file_name,
            "Under Review",
            datetime.now()
        ))
        conn.commit()
        conn.close()

        return redirect("/complaints/my")

    return render_template("ICC_complaint.html")


# ---------------- VIEW MY COMPLAINTS ----------------
@app.route("/complaints/my")
def my_complaints():
    conn = get_db()
    complaints = conn.execute(
        "SELECT * FROM complaints WHERE user_id=?",
        (session.get("user_id"),)
    ).fetchall()
    conn.close()

    return render_template("complaint_dashboard.html", complaints=complaints)


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
