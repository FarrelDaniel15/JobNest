import os
import sqlite3
import requests

from flask import Flask, flash, redirect, render_template, request, session, g
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# --- DATABASE SETUP (Defined BEFORE routes) ---

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "jobnest.db")

def get_db():
    """Helper to get the database connection using absolute path"""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE_PATH, timeout=20)
        g.db.row_factory = sqlite3.Row 
    return g.db

@app.teardown_appcontext
def close_db(error):
    """Automatically close the database connection at request end"""
    db = g.pop('db', None)
    if db is not None:
        db.close()


# --- DECORATORS & ROUTE HANDLERS ---

def login_required(f):
    """Decorate routes to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check if all fields are filled correctly
        if not username:
            return render_template("apology.html", message="Username must not be empty")
        elif not email:
            return render_template("apology.html", message="Email must not be empty")
        elif not password:
            return render_template("apology.html", message="Password must not be empty")
        elif not confirmation:
            return render_template("apology.html", message="Password confirmation must not be empty")
        elif password != confirmation:
            return render_template("apology.html", message="Password and confirmation do not match")

        db = get_db()
        
        # Check existing user
        cursor = db.execute("SELECT * FROM users WHERE name = ?", (username,))
        rows = cursor.fetchall()
        cursor2 = db.execute("SELECT * FROM users WHERE email = ?", (email,))
        rows2 = cursor2.fetchall()

        if len(rows) > 0:
            return render_template("apology.html", message="Username already exists")
        if len(rows2) > 0:
            return render_template("apology.html", message="Email already exists")

        # Hash password and store
        hashed_password = generate_password_hash(password)
        db.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
        db.commit()

        # Retrieve new user id for session
        cursor = db.execute("SELECT id FROM users WHERE name = ?", (username,))
        user = cursor.fetchone()
        session["user_id"] = user["id"]

        return redirect("/")
        
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if all fields are entered correctly
        if not username:
            return render_template("apology.html", message="Username must not be empty")
        elif not password:
            return render_template("apology.html", message="Password must not be empty")

        db = get_db()

        # Check if the entered password matches the account password
        cursor = db.execute("SELECT * FROM users WHERE name = ?", (username,))
        user = cursor.fetchone()

        if not user or not check_password_hash(user["password"], password):
            return render_template("apology.html", message="Invalid password or username")

        session["user_id"] = user["id"]
        return redirect("/dashboard")

    else:
        return render_template("login.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        company_name = request.form.get("company_name")
        job = request.form.get("job")
        salary = request.form.get("salary")
        date = request.form.get("date")
        status = request.form.get("status")
        website = request.form.get("website")
        location = request.form.get("location")
        notes = request.form.get("notes")

        # Check if the mandatory fields are already filled
        if not company_name or not job or not date or not status:
            return render_template("apology.html", message="Company name, job, date, and status field must not be empty")
        if not website:
            website = "-"
        if not location:
            location = "-"
        if not notes:
            notes = "-"

        # This line of code until before else will only run if there is no error or unfilled mandatory fields of inputs
        db = get_db()
        # Correct for standard sqlite3
        db.execute("INSERT INTO job (user_id, company_name, job_name, salary, date_applied, status, job_link, location, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (session["user_id"], company_name, job, salary, date, status, website, location, notes))
        db.commit()

        return redirect("/dashboard")
    else:
        return render_template("add.html")


@app.route("/delete", methods=["GET", "POST"])
def delete():
    db = get_db()

    job_id = request.args.get("id")
    if not job_id:
        return render_template("apology.html", message="Missing job information")

    db.execute("DELETE FROM job WHERE id = ? AND user_id = ?", (job_id, session["user_id"]))
    db.commit()

    return redirect("/dashboard")

    
@app.route("/edit", methods=["GET", "POST"])
def edit():
    db = get_db()

    if request.method == "POST":
        job_id = request.form.get("id")
        company_name = request.form.get("company_name")
        job = request.form.get("job")
        salary = request.form.get("salary")
        date = request.form.get("date")
        status = request.form.get("status")
        website = request.form.get("website")
        location = request.form.get("location")
        notes = request.form.get("notes")

        # Check if all of the fields are entered correctly
        if not company_name or not job or not date or not status:
            return render_template("apology.html", message="Company name, job, date, and status field must not be empty")
        if not website:
            website = "-"
        if not location:
            location = "-"
        if not notes:
            notes = "-"

        # This line of code until before else will only run if there is no error or unfilled mandatory fields of inputs
        db = get_db()
        # Correct for standard sqlite3
        db.execute("UPDATE job SET user_id = ?, company_name = ?, job_name = ?, salary = ?, date_applied = ?, status = ?, job_link = ?, location = ?, notes= ? WHERE user_id = ? AND id = ?", (session["user_id"], company_name, job, salary, date, status, website, location, notes, session["user_id"], job_id))
        db.commit()

        return redirect("/dashboard")
    else:
        job_id = request.args.get("id")
        if not job_id:
            return render_template("apology.html", message="Missing job information")

        cursor = db.execute("SELECT * FROM job WHERE id = ? AND user_id = ?", (job_id, session["user_id"]))
        job_dict = cursor.fetchone()

        if not job_dict:
            return render_template("apology.html", message="Missing job information")

        job_dict = dict(job_dict)
        
        return render_template("edit.html", job_dict=job_dict)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    db = get_db()
    job_data = db.execute("SELECT * FROM job WHERE user_id = ?", (session["user_id"],))

    return render_template("dashboard.html", job_data=job_data)

if __name__ == "__main__":
    app.run(debug=True)