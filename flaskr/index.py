import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

from flaskr.auth import login_required

from .helpers.form_helpers import form_filled_in

bp = Blueprint("index", __name__)

# This BP should handle ALL the routes that should be accessible to anyone, not only those with an account


@bp.route("/")
def index():
    # Dictionary for Jinja looping
    # TODO: ADD HREF LIST
    prefixes = ['wellefcher', 'explorer', 'pio', 'rover']
    text_values = ["Wëllefcher", "Explorer", "Pio", "Rover"]
    age_values = ["8 - 11 Joër", "11 - 14 Joër", "14 - 17 Joër", "17 - 23 Joër"]
    img_values = [url_for('static', filename = i) for i in ["images/wellefcher.jpeg", "images/avex.png", "images/pio.png", "images/rover.png"]]

    branches = {}

    for prefix, text, age, img in zip(prefixes, text_values, age_values, img_values):
        branches[prefix] = {
            f"text": text,
            f"age": age,
            f"img": img
        }

    # A test, I will have to create an html file that EXTENDS base.html to show actual content on the website
    return render_template("index/index.html", branches=branches)

@bp.route("/apply", methods=["GET", "POST"])
@login_required
def apply():
    # Get user info
    db = get_db()
    user_info = db.execute("SELECT * from user JOIN address ON user.id = address.user_id WHERE id = ?", (session["user_id"],)).fetchone()
    
    # POST REQUEST
    if request.method == "POST":
        print(user_info["first_name"])
        
        if user_info["scout_registration"] == "TRUE":
            flash("Dir sidd schon ugemellt!")
            return redirect(url_for("index.index"))
        
        else:
            # request form information (immutable object)
            form_info_immutable = request.form
            print(f"initial: {form_info_immutable}")
            
            # initialize dict (mutable object)
            form_info = {}
            
            # check for falsy input, strip input from leading and trailing whitespaces
            for info in form_info_immutable:
                form_info[info] = form_info_immutable[info].strip()

            # Connect to database
            db = get_db()
        
            try:
                # Update user table with child info
                db.execute("UPDATE user SET branch=?, allergies=?, diet=?, otherInformation=? WHERE id = ?", (form_info["branch"], form_info["allergies"], form_info["diet"], form_info["otherInformation"], session["user_id"]))
                
                # If parent_1 not already in the database, insert into parent table
                integrity_check = db.execute("SELECT * FROM parent WHERE email = ?", (form_info["email_p1"],)).fetchone()
                
                if integrity_check is None:
                    db.execute("INSERT INTO parent (first_name, last_name, phone_number, email) VALUES (?, ?, ?, ?)", (form_info["first_name_p1"], form_info["last_name_p1"], form_info["number_p1"], form_info["email_p1"]))
                
            except db.IntegrityError:
                flash("E Problem ass opgetrueden. Feeler Code 100.")
                return redirect(url_for("index.apply"))
            
            if "email_p2" in form_info:
                try:    
                    # If parent 2 is not already in the database, insert into parent table
                    integrity_check = db.execute("SELECT * FROM parent WHERE email = ?", (form_info["email_p2"],)).fetchone()
                
                    if integrity_check is None:
                        db.execute("INSERT INTO parent (first_name, last_name, phone_number, email) VALUES (?, ?, ?, ?)", (form_info["first_name_p2"], form_info["last_name_p2"], form_info["number_p2"], form_info["email_p2"]))
                
                except db.IntegrityError:
                    flash("E Problem ass opgetrueden. Feeler Code 101.")
                    return redirect(url_for("index.apply"))
            
            try:
                # Get parent email
                if "email_p2" in form_info:
                    # Link parent(s) with child
                    parent_id = db.execute("SELECT id FROM parent WHERE email = ? OR email = ?", (form_info["email_p1"], form_info["email_p2"]))
                else:
                    parent_id = db.execute("SELECT id FROM parent WHERE email = ?", (form_info["email_p1"], ))
                
                for id in parent_id:
                        db.execute("INSERT INTO parent_child (parent_id, child_id) VALUES (?, ?)", (id[0], session["user_id"]))
                    
            except db.IntegrityError:
                flash("E Problem ass opgetrueden. Feeler Code 102.")
                return redirect(url_for("index.apply"))
                
            # Update user database and set scout_registration to TRUE
            db.execute("UPDATE user SET scout_registration = ? WHERE id = ?", ("TRUE", session["user_id"]))
            
            # Commit database changes
            db.commit()

            # Return to home
            return redirect(url_for("index.index"))
    
    # GET REQUEST
    # Image dictionary for Jinja looping
    branch_images = {
        "wellefcher": url_for('static', filename='images/wellefcher.jpeg'),
        "explorer": url_for('static', filename='images/avex.png'),
        "pio": url_for('static', filename='images/pio.png'),
        "rover": url_for('static', filename='images/rover.png')
    }
    
    # Form questions
    questions = {
        1: "Ech sin domat averstanen, dass vu mengem Kand Fotoe gemaach gin.",
        2: "Ech sin domat averstanen, dass Fotoen, déi am Laf vu (Gruppen)Aktivitéiten vu mengem Kand gemach gin, op de soziale Medien (Facebook) vum Käler Scoutsgrupp gedeelt kenne gin.",
        3: "Ech sin domat averstanen, dass meng Email Adress an Telefonsnummer benotzt gin, fir vun de Cheffe kontaktéiert ze gin.",
        4: "Mäi Kand dierf no der Versammlung eleng heem goen."
    }
    
    return render_template("index/apply.html", questions=questions, user_info=user_info, branch_images=branch_images)

@bp.route("/contact")
def contact():
    return render_template("index/contact.html")