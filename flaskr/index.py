import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

from flaskr.auth import login_required

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

@bp.route("/apply")
@login_required
def apply():
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
    
    # Questions on form
    questions = {}
    questions[1] = "Ech sin domat averstanen, dass vu mengem Kand Fotoe gemaach gin."
    questions[2] = "Ech sin domat averstanen, dass Fotoen, déi am Laf vu (Gruppen)Aktivitéiten vu mengem Kand gemach gin, op de soziale Medien (Facebook) vum Käler Scoutsgrupp gedeelt kenne gin."
    questions[3] = "Ech sin domat averstanen, dass meng Email Adress an Telefonsnummer benotzt gin, fir vun de Cheffe kontaktéiert ze gin."
    questions[4] = "Mäi Kand dierf no der Versammlung eleng heem goen."
    
    return render_template("index/apply.html", questions=questions, user_info=user_info, branch_images=branch_images)

@bp.route("/contact")
def contact():
    return render_template("index/contact.html")
