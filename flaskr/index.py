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
    img_values = [url_for('static', filename = i) for i in ["Wellefcher_rgb.jpeg", "AvEx_rgb.png", "CaraPio_rgb.png", "RaRo_rgb.png"]]

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
    # POST REQUEST
    if request.method == "POST":
        
        # Form info: "form_info" is a dict containing three dicts
    
        form_info = {
            "child_info": {
                "branch": request.form.get("branch"),
                "allergies": request.form.get("allergies"),
                "diet": request.form.get("diet"),
                "other_information": request.form.get("other_information") 
            },
            
            "parent_1": {
                "last_name": request.form.get("last_name_p1").upper(),
                "first_name": request.form.get("first_name_p1").upper(),
                "phone_number": request.form.get("number_p1"),
                "email": request.form.get("email_p1")
            },
            
            "parent_2": {
                "last_name": request.form.get("last_name_p2").upper(),
                "first_name": request.form.get("first_name_p2").upper(),
                "phone_number": request.form.get("number_p2"),
                "email": request.form.get("email_p2")
            },
            
            "emergency": {
                "last_name": request.form.get("last_name_e").upper(),
                "first_name": request.form.get("first_name_e").upper(),
                "phone_number": request.form.get("number_e"),
                "phone": request.form.get("phone_e"),
                "email": request.form.get("email_e"),
                "house_number": request.form.get("house_number_e"),
                "street": request.form.get("street_e"),
                "town": request.form.get("town_e"),
                "country": request.form.get("country_e"),
                "zip": request.form.get("zip_e"),
            }
        }

        # Connect to database
        db = get_db()
        
        try:
            # Update user table with child info
            db.execute("UPDATE user SET branch=?, allergies=?, diet=?, otherInformation=? WHERE id = ?", (*form_info["child_info"].values(), session["user_id"]))
            
            # Insert parent_1 into parent table
            db.execute("INSERT INTO parent (user_id, first_name, last_name, phone_number, email) VALUES (?, ?, ?, ?, ?)", (session["user_id"], *form_info["parent_1"].values()))
            
            # Insert parent_2 into parent table (form_info["parent_2"] is itself a dict)
            if form_filled_in(form_info["parent_2"]):
                db.execute("INSERT INTO parent (user_id, first_name, last_name, phone_number, email) VALUES (?, ?, ?, ?, ?)", (session["user_id"], *form_info["parent_2"].values()))
                
                # If parent_2 exists, insert both parents into parent_child table
                parent_id = db.execute("SELECT id FROM parent WHERE user_id = ?", (session["user_id"],))
                
                for id in parent_id:
                    db.execute("INSERT INTO parent_child (parent_id, child_id) VALUES (?, ?)", (id[0], session["user_id"]))
            
            else:
                # Get parent id
                parent_id = db.execute("SELECT id FROM parent WHERE user_id = ?", (session["user_id"],))
                
                # Insert parent into parent_child table
                db.execute("INSERT INTO parent_child (parent_id, child_id) VALUES (?, ?)", (parent_id, session["user_id"]))

            # Commit at the end
            db.commit()
            
        except db.IntegrityError:
            flash("db.IntegrityError")
            return redirect(url_for("index.apply"))
            
        # If no error, save True to an "applied" variable because applying should only be possible ONCE:
        applied = True
            
        return redirect(url_for("index.index"))
    
    # GET REQUEST
    # Image dictionary for Jinja looping
    branch_images = {
        "wellefcher": url_for('static', filename='Wellefcher_rgb.jpeg'),
        "explorer": url_for('static', filename='AvEx_rgb.png'),
        "pio": url_for('static', filename='Carapio_rgb.png'),
        "rover": url_for('static', filename='RaRo_rgb.png')
    }
    # Connect to database
    db = get_db()
    
    # Get user data
    user_info = db.execute("SELECT * from user JOIN address ON user.id = address.user_id WHERE id = ?", (session["user_id"],)).fetchone()
    
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
