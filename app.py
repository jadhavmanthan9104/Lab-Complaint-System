from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret_key"  # Required for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------ DATABASE MODELS ------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(20))  # student, admin, technician, icc

# Create the database tables
with app.app_context():
    db.create_all()

# ------------------ ROUTES ------------------

@app.route('/')
def login_page():
    return render_template('login.html')
@app.route('/student/signup')
def student_signup():
    return render_template('student.html')

@app.route('/admin/signup')
def admin_signup():
    return render_template('admin.html')


# ---------------- LOGIN ----------------
@app.route('/', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']

    user = User.query.filter_by(email=email, password=password, role=role).first()
    if user:
        session['user_id'] = user.id
        session['role'] = user.role
        # Redirect based on role
        if role == 'student':
            return redirect('/student/dashboard')
        elif role == 'admin':
            return redirect('/admin/dashboard')
        elif role == 'technician':
            return redirect('/technician/dashboard')
        elif role == 'icc':
            return redirect('/icc/dashboard')
    else:
        return render_template('login.html', error="Invalid credentials")

# ---------------- STUDENT SIGNUP ----------------
@app.route('/student/signup', methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name, email=email, password=password, role='student')
        db.session.add(new_user)
        db.session.commit()

        return redirect('/')

    return render_template('student.html')


# ---------------- ADMIN SIGNUP ----------------
@app.route('/admin/signup', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        # You can validate OTP here if implemented
        new_user = User(name=name, email=email, password=password, role='admin')
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    return render_template('admin.html')

# ---------------- DASHBOARDS ----------------
@app.route('/student/dashboard')
def student_dashboard():
    return "<h2>Welcome Student</h2>"

@app.route('/admin/dashboard')
def admin_dashboard():
    return "<h2>Welcome Admin</h2>"

@app.route('/technician/dashboard')
def technician_dashboard():
    return "<h2>Welcome Technician</h2>"

@app.route('/icc/dashboard')
def icc_dashboard():
    return "<h2>Welcome ICC</h2>"

# ---------------- RUN APP ----------------
if __name__ == '__main__':
    app.run(debug=True)
