import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
#from werkzeug.security import check_password_hash, generate_password_hash
#from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.forms import ScoutForm, TutorForm, EmergencyForm, QuestionsForm
from collections import OrderedDict
from .classes import Scout, Tutor

# Email imports
from .mail import mail
from flask_mail import Message
from pandas import DataFrame
from openpyxl import Workbook
import os

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

@bp.route("/contact", methods=["GET", "POST"])

def apply():
    return render_template("index/contact.html")

@bp.route("/apply", methods=["GET", "POST"])
def contact():
    # Initialize session data
    for session_name in ["form_user_data", "form_tutor_1_data", "form_tutor_2_data", "form_emergency_data"]:
        if session.get(session_name) is None:
            session[session_name] = OrderedDict()

    # Instantiate forms
    form_user = ScoutForm()
    form_tutor = TutorForm()
    form_emergency = EmergencyForm()
    form_questions = QuestionsForm()
    
    # Define questions to ask user for approval
    questions = {
        "pictures": "Ech sin domat averstanen, dass vu mengem Kand Fotoe gemaach gin.",
        "social_media": "Ech sin domat averstanen, dass Fotoen, déi am Laf vu (Gruppen)Aktivitéiten vu mengem Kand gemach gin, op de soziale Medien (Facebook) vum Käler Scoutsgrupp gedeelt kenne gin.",
        "contact": "Ech sin domat averstanen, dass meng Email Adress an Telefonsnummer benotzt gin, fir vun de Cheffe kontaktéiert ze gin.",
        "home_alone": "Mäi Kand dierf no der Versammlung eleng heem goen."
    }
    
    # Concatenate forms and corresponding submit buttons (see definition in forms.py)
    forms = [form_user, form_tutor, form_emergency, form_questions]
    submit_buttons = ["submit_1", "submit_2", "submit_3", "submit_4"]
    
    if request.method == "POST":
        # Loop through forms
        for form, submit_button in zip(forms, submit_buttons):
            # Check pressed submit button
            if getattr(form, submit_button).data:
                # If form is VALID
                if form.validate():
                    # Save form data in session using dedicated class
                    if form.form_name == "form_user":
                        session[form.form_name + "_data"] = Scout(*[form.data[key] for key in form.field_names_scout])
                        # Render next form tab
                        return render_template("index/apply.html", active_tab = form.redirect_tab, form_user=form_user, form_tutor=form_tutor, form_emergency=form_emergency, form_questions=form_questions, questions=questions, session=session,
                                                                                user_data=session["form_user_data"], tutor_1_data=session["form_tutor_1_data"], tutor_2_data = session["form_tutor_2_data"], urgent_data=session["form_emergency_data"])
                    elif form.form_name == "form_tutor":
                        session[form.form_name + "_1_data"] = Tutor(*[form.data[key] for key in form.field_names_tutor_1])
                        session[form.form_name + "_2_data"] = Tutor(*[form.data[key] for key in form.field_names_tutor_2])
                        # Render next form tab
                        return render_template("index/apply.html", active_tab = form.redirect_tab, form_user=form_user, form_tutor=form_tutor, form_emergency=form_emergency, form_questions=form_questions, questions=questions, session=session,
                                                                                user_data=session["form_user_data"], tutor_1_data=session["form_tutor_1_data"], tutor_2_data = session["form_tutor_2_data"], urgent_data=session["form_emergency_data"])
                    elif form.form_name == "form_emergency":
                        session[form.form_name + "_data"] = Tutor(*[form.data[key] for key in form.field_names_emergency])
                        # Render next form tab
                        return render_template("index/apply.html", active_tab = form.redirect_tab, form_user=form_user, form_tutor=form_tutor, form_emergency=form_emergency, form_questions=form_questions, questions=questions, session=session,
                                                                                user_data=session["form_user_data"], tutor_1_data=session["form_tutor_1_data"], tutor_2_data = session["form_tutor_2_data"], urgent_data=session["form_emergency_data"])
                    # Last form (form_questions)
                    else:
                        session[form.form_name + "_data"] = form.data
                        
                        # Create objects in memory (if done previously, the new requests taking place on form submits delete it from memory)
                        scout = session["form_user_data"]
                        tutor_1 = session["form_tutor_1_data"]
                        tutor_2 = session["form_tutor_2_data"]
                        tutor_3 = session["form_emergency_data"]
                        
                        # Connect to database
                        db = get_db()
                        
                        # Add scout to user table
                        try:
                            db.execute("INSERT INTO user (first_name, last_name, birthday, gender, number, branch, email, allergies, diet, other_information) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                   (scout["first_name"], scout["last_name"], scout["birthday"], scout["gender"], scout["number"], scout["branch"], scout["email"], scout["allergies"], scout["diet"], scout["other"]))
                        except db.IntegrityError:
                            flash("E Feeler ass opgetrueden. Feeler Code 100.")
                            
                        # Get ID of added scout
                        try:
                            scout_id = db.execute("SELECT id FROM user WHERE first_name = ? AND last_name = ? AND birthday = ?", (scout["first_name"], scout["last_name"], scout["birthday"])).fetchone()
                        except db.IntegrityError:
                            flash("E Feeler ass opgetrueden. Feeler Code 101.")
                            
                        # Add address to address table
                        try:
                            db.execute("INSERT INTO address (house_number, street, town, zip, country, user_id) VALUES (?, ?, ?, ?, ?, ?)", (scout["house_number"], scout["street"], scout["town"], scout["zip"], scout["country"], scout_id[0]))
                        except db.IntegrityError:
                            flash("E Feeler ass opgetrueden. Feeler Code 102.")
                        
                        # Add tutor_1 to parent table
                        # Check if tutor exists
                        exists = db.execute("SELECT id FROM parent WHERE phone_number = ? AND email = ?", (tutor_1["number"], tutor_1["email"])).fetchone()
                        
                        # If tutor does not exist, add to table
                        if exists is None:
                            try:
                                db.execute("INSERT INTO parent (first_name, last_name, phone_number, email) VALUES (?, ?, ?, ?)", (tutor_1["first_name"], tutor_1["last_name"], tutor_1["number"], tutor_1["email"]))
                            except db.IntegrityError:
                                flash("E Feeler ass opgetrueden. Feeler Code 103.")
                        
                        # Get id tutor 1
                        tutor_1_id = db.execute("SELECT id FROM parent WHERE first_name = ? AND last_name = ? AND phone_number = ? AND email = ?", (tutor_1["first_name"], tutor_1["last_name"], tutor_1["number"], tutor_1["email"])).fetchone()
                            
                            
                        # Add tutor 2 to parent table
                        # Check if tutor was submitted
                        if tutor_2["first_name"] != '':
                            # Check if tutor exists
                            exists = db.execute("SELECT id FROM parent WHERE phone_number = ? AND email = ?", (tutor_2["number"], tutor_2["email"])).fetchone()
                            
                            # If tutor does not exist, add to table
                            if exists is None:
                                try:
                                    db.execute("INSERT INTO parent (first_name, last_name, phone_number, email) VALUES (?, ?, ?, ?)", (tutor_2["first_name"], tutor_2["last_name"], tutor_2["number"], tutor_2["email"]))
                                except db.IntegrityError:
                                    flash("E Feeler ass opgetrueden. Feeler Code 107.")
                        
                        # Get id of tutor 2
                            tutor_2_id = db.execute("SELECT id FROM parent WHERE first_name = ? AND last_name = ? AND phone_number = ? AND email = ?", (tutor_2["first_name"], tutor_2["last_name"], tutor_2["number"], tutor_2["email"])).fetchone()
                        
                        # Add tutor 3 to emergency table
                        # Check if tutor 3 exists
                        exists = db.execute("SELECT id FROM emergency WHERE phone_number = ? AND email = ?", (tutor_3["number"], tutor_3["email"])).fetchone()
                        
                        # If tutor 3 does not exist, add to table
                        if exists is None:
                            try:
                                db.execute("INSERT INTO emergency (first_name, last_name, phone_number, email) VALUES (?, ?, ?, ?)", (tutor_3["first_name"], tutor_3["last_name"], tutor_3["number"], tutor_3["email"]))
                            except db.IntegrityError:
                                flash("E Feeler ass opgetrueden. Feeler Code 105.")
                        
                        # Get id of tutor 3
                        tutor_3_id = db.execute("SELECT id FROM emergency WHERE first_name = ? AND last_name = ? AND phone_number = ? AND email = ?", (tutor_3["first_name"], tutor_3["last_name"], tutor_3["number"], tutor_3["email"])).fetchone()
                        
                        # Link tutor-child-emergency_contact
                        try:
                            db.execute("INSERT INTO parent_child_emergency (parent_id, child_id, emergency_id) VALUES (?, ?, ?)", (tutor_1_id[0], scout_id[0], tutor_3_id[0]))
                            if tutor_2_id:
                                db.execute("INSERT INTO parent_child_emergency (parent_id, child_id, emergency_id) VALUES (?, ?, ?)", (tutor_2_id[0], scout_id[0], tutor_3_id[0]))
                        except db.IntegrityError:
                            flash("E Feeler ass opgetrueden. Feeler Code 106.")
                        
                    # Commit database changes
                    db.commit()
                    
                    # Clear session
                    for key in ["form_user_data", "form_tutor_1_data", "form_tutor_2_data", "form_emergency_data"]:
                        session.pop(key, default=None)
                    
                    # Flash success message
                    flash("Dir gouft ugemellt!")
                    
                    # Redirect to home page
                    return redirect(url_for("index.index"))
                
                # If form is INVALID
                else:
                    return render_template("index/apply.html", active_tab=form.form_name, form_user=form_user, form_tutor=form_tutor, form_emergency=form_emergency, form_questions=form_questions, questions=questions,
                                           user_data=session["form_user_data"], tutor_1_data=session["form_tutor_1_data"], tutor_2_data=session["form_tutor_2_data"], urgent_data=session["form_emergency_data"])
    if request.method == "GET":
        return render_template("index/apply.html", active_tab="form_user", form_questions=form_questions, form_user=form_user, form_tutor=form_tutor, form_emergency=form_emergency, user_data=session["form_user_data"], tutor_1_data=session["form_tutor_1_data"], tutor_2_data=session["form_tutor_2_data"], urgent_data=session["form_emergency_data"], questions=questions)