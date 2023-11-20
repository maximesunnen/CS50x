import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
#from werkzeug.security import check_password_hash, generate_password_hash
#from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.forms import ScoutForm, TutorForm, EmergencyForm, QuestionsForm
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
            session[session_name] = {}
    
    # Instantiate forms
    form_user = ScoutForm()
    form_tutor = TutorForm()
    form_emergency = EmergencyForm()
    form_questions = QuestionsForm()
    
    # Questions
    questions = {
        "pictures": "Ech sin domat averstanen, dass vu mengem Kand Fotoe gemaach gin.",
        "social_media": "Ech sin domat averstanen, dass Fotoen, déi am Laf vu (Gruppen)Aktivitéiten vu mengem Kand gemach gin, op de soziale Medien (Facebook) vum Käler Scoutsgrupp gedeelt kenne gin.",
        "contact": "Ech sin domat averstanen, dass meng Email Adress an Telefonsnummer benotzt gin, fir vun de Cheffe kontaktéiert ze gin.",
        "home_alone": "Mäi Kand dierf no der Versammlung eleng heem goen."
    }
    
    # Forms and submit buttons as list (see definition in forms.py)
    forms = [form_user, form_tutor, form_emergency, form_questions]
    submit_buttons = ["submit_1", "submit_2", "submit_3", "submit_4"]
    
    if request.method == "POST":
        # Loop through forms
        for form, submit_button in zip(forms, submit_buttons):
            # Check pressed submit button
            if getattr(form, submit_button).data:
                # If form is VALID
                if form.validate():
                    # Save form data in session using dedicated class [saving in session leads to SERIALIZATION, custom encoder in __init__.py]
                    if form.name == "form_user":
                        scout = Scout(*[form.data[key] for key in form.field_names_scout])
                        session[form.name + "_data"] = scout
                        
                        # Render next form tab
                        return render_template("index/apply.html", active_tab = form.redirect_tab, form_user=form_user, form_tutor=form_tutor, form_emergency=form_emergency, form_questions=form_questions, questions=questions, session=session,
                                                                                user_data=session["form_user_data"], tutor_1_data=session["form_tutor_1_data"], tutor_2_data = session["form_tutor_2_data"], urgent_data=session["form_emergency_data"])
                    elif form.name == "form_tutor":
                        tutor_1 = Tutor(*[form.data[key] for key in form.field_names_tutor_1])
                        session[form.name + "_1_data"] = tutor_1
                        
                        tutor_2 = Tutor(*[form.data[key] for key in form.field_names_tutor_2])
                        session[form.name + "_2_data"] = tutor_2
                        
                        # Render next form tab
                        return render_template("index/apply.html", active_tab = form.redirect_tab, form_user=form_user, form_tutor=form_tutor, form_emergency=form_emergency, form_questions=form_questions, questions=questions, session=session,
                                                                                user_data=session["form_user_data"], tutor_1_data=session["form_tutor_1_data"], tutor_2_data = session["form_tutor_2_data"], urgent_data=session["form_emergency_data"])
                    elif form.name == "form_emergency":
                        tutor_3 = Tutor(*[form.data[key] for key in form.field_names_emergency])
                        session[form.name + "_data"] = tutor_3
                        
                        # Render next form tab
                        return render_template("index/apply.html", active_tab = form.redirect_tab, form_user=form_user, form_tutor=form_tutor, form_emergency=form_emergency, form_questions=form_questions, questions=questions, session=session,
                                                                                user_data=session["form_user_data"], tutor_1_data=session["form_tutor_1_data"], tutor_2_data = session["form_tutor_2_data"], urgent_data=session["form_emergency_data"])
                    # Last form (form_questions)
                    else:
                        session[form.name + "_data"] = form.data
                        
                        # Instantiate objects using from_dict method
                        scout = Scout.from_dict(session["form_user_data"])
                        tutor_1 = Tutor.from_dict(session["form_tutor_1_data"])
                        tutor_2 = Tutor.from_dict(session["form_tutor_2_data"])
                        tutor_3 = Tutor.from_dict(session["form_emergency_data"])
                        questions = session["form_questions_data"]
                        
                        # Connect to database
                        db = get_db()
                        
                        # Add scout to user table
                        try:
                            db.execute("INSERT INTO user (first_name, last_name, birthday, gender, number, branch, email, allergies, diet, other_information) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                   (scout.first_name, scout.last_name, scout.birthday, scout.gender, scout.number, scout.branch, scout.email, scout.allergies, scout.diet, scout.other))
                        except Exception as e:
                            print(f"An error occurred (Error Code 100): {e}")
                            
                        # Get ID of added scout
                        try:
                            scout_id = db.execute("SELECT id FROM user WHERE first_name = ? AND last_name = ? AND birthday = ?", (scout.first_name, scout.last_name, scout.birthday)).fetchone()
                        except Exception as e:
                            print(f"An error occurred (Error Code 101): {e}")
                            
                        # Add address to address table
                        try:
                            db.execute("INSERT INTO address (house_number, street, town, zip, country, user_id) VALUES (?, ?, ?, ?, ?, ?)", (scout.house_number, scout.street, scout.town, scout.zip, scout.country, scout_id[0]))
                        except Exception as e:
                            print(f"An error occurred (Error Code 102): {e}")
                        
                        # Add tutor_1 to parent table
                        # Check if tutor exists
                        tutor_1_id = db.execute("SELECT id FROM parent WHERE first_name = ? AND last_name = ? AND phone_number = ? AND email = ?", (tutor_1.first_name, tutor_1.last_name, tutor_1.number, tutor_1.email)).fetchone()
                        # If tutor does not exist, add to table
                        if tutor_1_id is None:
                            try:
                                db.execute("INSERT INTO parent (first_name, last_name, phone_number, email) VALUES (?, ?, ?, ?)", (tutor_1.first_name, tutor_1.last_name, tutor_1.number, tutor_1.email))
                                # Get tutor_1 id
                                tutor_1_id = db.execute("SELECT id FROM parent WHERE first_name = ? AND last_name = ? AND phone_number = ? AND email = ?", (tutor_1.first_name, tutor_1.last_name, tutor_1.number, tutor_1.email)).fetchone()
                            except Exception as e:
                                print(f"An error occurred (Error Code 103): {e}")
                        
                        # Add tutor 2 to parent table
                        # Check if tutor was submitted
                        if tutor_2.first_name != '':
                            # Check if tutor exists
                            tutor_2_id = db.execute("SELECT id FROM parent WHERE first_name = ? AND last_name = ? AND phone_number = ? AND email = ?", (tutor_2.first_name, tutor_2.last_name, tutor_2.number, tutor_2.email)).fetchone()
                            # If tutor does not exist, add to table
                            if tutor_2_id is None:
                                try:
                                    db.execute("INSERT INTO parent (first_name, last_name, phone_number, email) VALUES (?, ?, ?, ?)", (tutor_2.first_name, tutor_2.last_name, tutor_2.number, tutor_2.email))
                                    # Get tutor_2 id
                                    tutor_2_id = db.execute("SELECT id FROM parent WHERE first_name = ? AND last_name = ? AND phone_number = ? AND email = ?", (tutor_2.first_name, tutor_2.last_name, tutor_2.number, tutor_2.email)).fetchone()
                                except Exception as e:
                                    print(f"An error occurred (Error Code 104): {e}")
                        
                        # Add tutor 3 to emergency table
                        # Check if tutor 3 exists
                        tutor_3_id = db.execute("SELECT id FROM emergency WHERE first_name = ? AND last_name = ? AND phone_number = ? AND email = ?", (tutor_3.first_name, tutor_3.last_name, tutor_3.number, tutor_3.email)).fetchone()

                        # If tutor 3 does not exist, add to table
                        if tutor_3_id is None:
                            try:
                                db.execute("INSERT INTO emergency (first_name, last_name, phone_number, email) VALUES (?, ?, ?, ?)", (tutor_3.first_name, tutor_3.last_name, tutor_3.number, tutor_3.email))
                                # Get tutor_3 id 
                                tutor_3_id = db.execute("SELECT id FROM emergency WHERE first_name = ? AND last_name = ? AND phone_number = ? AND email = ?", (tutor_3.first_name, tutor_3.last_name, tutor_3.number, tutor_3.email)).fetchone()

                            except Exception as e:
                                print(f"An error occurred (Error Code 105): {e}")

                        # Link tutor-child-emergency_contact
                        try:
                            db.execute("INSERT INTO parent_child_emergency (parent_id, child_id, emergency_id) VALUES (?, ?, ?)", (tutor_1_id[0], scout_id[0], tutor_3_id[0]))
                            if tutor_2_id:
                                db.execute("INSERT INTO parent_child_emergency (parent_id, child_id, emergency_id) VALUES (?, ?, ?)", (tutor_2_id[0], scout_id[0], tutor_3_id[0]))
                        except db.IntegrityError:
                            flash("E Feeler ass opgetrueden. Feeler Code 106.")
                            
                        # Add answers to questions to database
                        try:
                            db.execute("INSERT INTO data_protection (child_id, pictures, social_media, contact, home_alone) VALUES (?, ?, ?, ?, ?)", (scout_id[0], questions["pictures"], questions["social_media"], questions["contact"], questions["home_alone"]))
                        except db.IntegrityError:
                            flash("E Feeler ass opgetrueden. Feeler Code 107.")

                        
                    # Commit database changes
                    db.commit()
                    
                    # Send Email
                    # Email message
                    msg = Message("Nei Umeldung bei den Wëllefcher", sender="peter@mailtrap.io", recipients=["paul@mailtrap.io"])
                    
                    # Email attachment
                    # Excel columns
                    objects = [scout, tutor_1, tutor_2, tutor_3]
                    columns = [key for obj in objects for key in obj.__dict__] + form_questions.field_names_questions
                    print(columns)
                    # Excel data
                    scout_data = [getattr(scout, key) for key in scout.__dict__]
                    tutor_1_data = [getattr(tutor_1, key) for key in tutor_1.__dict__]
                    tutor_2_data = [getattr(tutor_2, key) for key in tutor_2.__dict__]
                    tutor_3_data = [getattr(tutor_3, key) for key in tutor_3.__dict__]
                    questions_data = list(session["form_questions_data"].values())[:4]
                    
                    # Excel dataframe
                    df = DataFrame([scout_data + tutor_1_data + tutor_2_data + tutor_3_data + questions_data], columns=columns)
                    print(df)
                    
                    # Temporary xlsx file
                    tmp_xlsx = Workbook().save("flaskr/tmp.xlsx")
                    
                    # Data frame to Excel
                    df.to_excel("flaskr/tmp.xlsx", index=False)
                    
                    # Attach file to email message
                    with open("flaskr/tmp.xlsx", "rb") as fp:
                        msg.attach("tmp.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", fp.read())
                        
                    # Send mail
                    mail.send(msg)
                    
                    # Remove temporary file
                    os.remove("flaskr/tmp.xlsx")
                    
                    # Clear session information
                    for key in ["form_user_data", "form_tutor_1_data", "form_tutor_2_data", "form_emergency_data"]:
                        session.pop(key, default=None)
                    
                    # Flash success message
                    flash("Dir gouft ugemellt!")
                    
                    # Redirect to home page
                    return redirect(url_for("index.index"))
                
                # If form is INVALID
                else:
                    return render_template("index/apply.html", active_tab=form.name, form_user=form_user, form_tutor=form_tutor, form_emergency=form_emergency, form_questions=form_questions, questions=questions,
                                           user_data=session["form_user_data"], tutor_1_data=session["form_tutor_1_data"], tutor_2_data=session["form_tutor_2_data"], urgent_data=session["form_emergency_data"])
    if request.method == "GET":
        return render_template("index/apply.html", active_tab="form_user", form_questions=form_questions, form_user=form_user, form_tutor=form_tutor, form_emergency=form_emergency, user_data=session["form_user_data"], tutor_1_data=session["form_tutor_1_data"], tutor_2_data=session["form_tutor_2_data"], urgent_data=session["form_emergency_data"], questions=questions)