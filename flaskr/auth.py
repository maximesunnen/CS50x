import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None
        
        # Connect to database
        db = get_db()
        
        if not username:
            error = "Username is missing."
            
        elif not password:
            error = "Password is missing"
            
        if error is None:
            try:
                # db.execute and db.commit are part of the database connection object returned by get_db()
                db.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, generate_password_hash(password)))
                db.commit()
            
            except db.IntegrityError:
                error = f"User {username} already exists."
            
            return redirect(url_for("auth.login"))
        
        flash(error)
    
    questions = {}
    questions[1] = "Ech sin domat averstanen, dass vu mengem Kand Fotoe gemaach gin."
    questions[2] = "Ech sin domat averstanen, dass Fotoen, déi am Laf vu (Gruppen)Aktivitéiten vu mengem Kand gemach goufen, op de soziale Medien (Facebook) vum Käler Scoutsgrupp gedeelt kenne gin."
    questions[3] = "Ech sin domat averstanen, dass meng Email Adress an Telefonsnummer benotzt gin, fir vun de Cheffe kontaktéiert ze gin."
    questions[4] = "Mäi Kand dierf no der Versammlung eleng heem goen."
        
    return render_template("auth/register.html", questions=questions)

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
    return render_template("auth/login.html")

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