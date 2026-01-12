from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3, os

app = Flask(__name__)
app.secret_key = "secret123"

DB_NAME = "database.db"

# ---------------- DATABASE SETUP ----------------
def init_db():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS lab_complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        lab TEXT,
        category TEXT,
        description TEXT,
        image TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS icc_complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        type TEXT,
        incident_date TEXT,
        description TEXT,
        evidence TEXT,
        counseling TEXT,
        status TEXT DEFAULT 'Under Review'
    )
    """)

    con.commit()
    con.close()

init_db()

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM users WHERE email=? AND password=? AND role=?",
            (email, password, role)
        )
        user = cur.fetchone()
        con.close()

        if user:
            session["user_id"] = user[0]
            session["role"] = user[4]

            if role == "Student":
                return redirect("/student")
            elif role == "Technician":
                return redirect("/technician")
            else:
                return redirect("/admin")

        return "Invalid Login"

    return render_template("login.html")

# ---------------- STUDENT SIGNUP ----------------
@app.route("/student_signup", methods=["GET", "POST"])
def student_signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        cur.execute(
            "INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)",
            (name, email, password, "Student")
        )
        con.commit()
        con.close()

        return redirect("/")

    return render_template("student_signup.html")

# ---------------- ADMIN SIGNUP ----------------
@app.route("/admin_signup", methods=["GET", "POST"])
def admin_signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        cur.execute(
            "INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)",
            (name, email, password, "Admin")
        )
        con.commit()
        con.close()

        return redirect("/")

    return render_template("admin_signup.html")

# ---------------- DASHBOARDS ----------------
@app.route("/student")
def student_dashboard():
    return render_template("student_dashboard.html")

@app.route("/technician")
def technician_dashboard():
    return render_template("technician_dashboard.html")

@app.route("/admin")
def admin_dashboard():
    return render_template("admin_dashboard.html")

# ---------------- LAB COMPLAINT ----------------
@app.route("/lab_complaint", methods=["GET", "POST"])
def lab_complaint():
    if request.method == "POST":
        lab = request.form["lab"]
        category = request.form["category"]
        description = request.form["description"]

        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        cur.execute(
            """INSERT INTO lab_complaints 
               (student_id,lab,category,description) 
               VALUES (?,?,?,?)""",
            (session["user_id"], lab, category, description)
        )
        con.commit()
        con.close()

        return redirect("/status")

    return render_template("lab_complaint.html")

# ---------------- ICC COMPLAINT ----------------
@app.route("/icc_complaint", methods=["GET", "POST"])
def icc_complaint():
    if request.method == "POST":
        ctype = request.form["type"]
        date = request.form["date"]
        desc = request.form["description"]
        counseling = request.form["counseling"]

        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        cur.execute(
            """INSERT INTO icc_complaints
               (student_id,type,incident_date,description,counseling)
               VALUES (?,?,?,?,?)""",
            (session["user_id"], ctype, date, desc, counseling)
        )
        con.commit()
        con.close()

        return redirect("/status")

    return render_template("icc_complaint.html")

# ---------------- COMPLAINT STATUS ----------------
@app.route("/status")
def complaint_status():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute(
        "SELECT id, lab, category, status FROM lab_complaints WHERE student_id=?",
        (session["user_id"],)
    )
    complaints = cur.fetchall()
    con.close()

    return render_template("complaint_status.html", complaints=complaints)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
