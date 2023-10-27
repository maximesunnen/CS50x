import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # user info dictionary
        user_info = {
            "first_name": request.form.get("first_name").upper(),
            "last_name":request.form.get("last_name").upper(),
            "username": request.form.get("username"),
            "password": request.form.get("password"),
            "password_confirm": request.form.get("passwordConfirm"),
            "birthday": request.form.get("birthday"),
            "gender": request.form.get("gender").upper(),
            "house_number": request.form.get("house_number"),
            "street": request.form.get("street").upper(),
            "town": request.form.get("town").upper(),
            "country": request.form.get("country"),
            "zip": request.form.get("zip"),
            "conditions": request.form.get("conditionsCheck")
        }
        
        # If falsy input, return register.html
        for info in user_info:
            if not user_info[info]:
                flash("Fëllt all d'Felder w.e.g aus")
                return render_template("auth/register.html")
        
        # If passwords not identical, return register.html
        if user_info["password"] != user_info["password_confirm"]:
            flash("Dir hudd zwee verschidden Passwieder agin.")
            return render_template("auth/register.html")
            
        # Initialize error to None:
        error = None
        
        # Connect to database
        db = get_db()
        
        try:
            # `db.execute` and `db.commit`: part of database connection object returned by `get_db()`
            
            # insert into user table
            db.execute("INSERT INTO user (username, first_name, last_name, password, birthday, gender) VALUES (?, ?, ?, ?, ?, ?)", (user_info["username"], user_info["first_name"], user_info["last_name"], generate_password_hash(user_info["password"]), user_info["birthday"], user_info["gender"],))
            
        except db.IntegrityError:
            error = f"User {user_info['username']} gëtt et schon."
            flash (error)
            return render_template("auth/register.html", txt_color="text-danger")
            
        try:
            # catch id
            id = db.execute("SELECT id FROM user WHERE username = ?", (user_info["username"],)).fetchone()[0]

            # insert into address table
            db.execute("INSERT INTO address (user_id, house_number, street, town, country, zip) VALUES (?, ?, ?, ?, ?, ?)", (id, user_info["house_number"], user_info["street"], user_info["town"], user_info["country"], user_info["zip"],))
            
        except db.IntegrityError:
            error = f"Database integrity error at address table insertion"
            flash(error)
            return render_template("auth/register.html", txt_color="text-danger")
        
        # commit db query
        db.commit()
        
        # Flash success message and redirect to login
        flash("Dir gouft registréiert!")
        return redirect(url_for("auth.login"))

    # GET
    return render_template("auth/register.html")

@bp.route("/login", methods = ["GET", "POST"]) # endpoint argument omitted: defaults view function name ('login')
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
         
        error = None
        
        if not username:
            error = "Usernumm feelt."
            
        elif not password:
            error = "Passwuert feelt."
            
        # Connect to database
        db = get_db()
        
        user = db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone() 
            # (username,): trailing comma to create single-element tuple
            # fetchone(): selects one row of query
            # no db.commit() needed because database not modified
            
        if not user:
            error = "Usernumm gëtt et nët."
        
        elif not check_password_hash(user["password"], password):
            error = "Falscht Passwuert."
        
        if error == None:
            # Add session
            session.clear()
            session["user_id"] = user["id"]
            
            return redirect(url_for("index.index"))
        
        else:
            flash(error)
            return render_template("auth/login.html", txt_color="text-danger")
        
    # GET
    return render_template("auth/login.html", txt_color="text-success")

# Before each request, check if user is logged in. Yes: save user information in g.user; No: save None in g.user
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id == None:
        g.user = None
    else:
        g.user = get_db().execute("SELECT * FROM USER WHERE id = ?", (user_id,)).fetchone()

# Log the user out by clearing the session
@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# Define login decorator
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

# Account view
@bp.route("/account")
@login_required
def account():
    return render_template("auth/account.html")

