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
            "first_name": request.form.get("firstName"),
            "last_name":request.form.get("lastName"),
            "username": request.form.get("username"),
            "password": request.form.get("password"),
            "password_confirm": request.form.get("passwordConfirm"),
            "birthday": request.form.get("birthDate"),
            "gender": request.form.get("gender"),
            "house_number": request.form.get("houseNumber"),
            "street": request.form.get("street"),
            "town": request.form.get("town"),
            "country": request.form.get("country"),
            "zip": request.form.get("zip"),
            "conditions": request.form.get("conditionsCheck")
        }
        
        # if any input is false (None or empty string), return register.html; otherwise redirect to login
        for info in user_info:
            if not user_info[info]:
                flash("Fëllt all d'Felder w.e.g aus")
                return render_template("auth/register.html")
        
        # initialize error to None
        error = None
        
        # Check if both passwords are identical
        if user_info["password"] != user_info["password_confirm"]:
            error = "Dir hudd zwee verschidden Passwieder agin."
            
        else:
            # Connect to database
            db = get_db()
        
        if error is None:
            try:
                # `db.execute` and `db.commit`: part of database connection object returned by `get_db()`
                db.execute("INSERT INTO user (username, firstName, lastName, password, birthday, gender) VALUES (?, ?, ?, ?, ?, ?)", (user_info["username"], user_info["first_name"], user_info["last_name"], generate_password_hash(user_info["password"]), user_info["birthday"], user_info["gender"]))
                db.commit()
            
            except db.IntegrityError:
                error = f"User {user_info['username']} gëtt et schon."
            
            else:
                flash("Dir gouft registréiert!")
                return redirect(url_for("auth.login"))
            
        flash(error)
        return redirect(url_for("auth.register"))

    # GET
    return render_template("auth/register.html", txt_color="text-danger")

@bp.route("/login", methods = ["GET", "POST"]) # endpoint argument omitted, therefore endpoint defaults to the name of the view function (here login)
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        error = None
        
        if not username:
            error = "Username missing."
            
        elif not password:
            error = "Password missing."
        
        # Connect to database
        db = get_db

        user = db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone() 
            # (username,): trailing comma to create single-element tuple
            # fetchone(): selects one row of query
            # no db.commit() needed because database not modified
            
        if not user:
            error = "Username does not exist."
        
        elif not check_password_hash(user["password"], password):
            error = "Wrong password."
            
        if error == None:
            # Add session
            session.clear()
            session["user_id"] = user["id"]
            
            return redirect(url_for("index"))
        
        flash(error)
    
    # If no redirect to "index", render login template again
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
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Define login decorator
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view