import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
#from flaskr.auth import login_required
from .helpers.form_helpers import form_filled_in
from flaskr.forms import userForm, tutorForm, urgentForm, questionsForm
from .mail import mail
from flask_mail import Message
from collections import OrderedDict

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
    for session_name in ["form_user_data", "form_tutor_data", "form_urgent_data"]:
        if session.get(session_name) is None:
            session[session_name] = OrderedDict()

    # Instantiate forms
    form_user = userForm()
    form_tutor = tutorForm()
    form_urgent = urgentForm()
    form_questions = questionsForm()
    
    # Define questions to ask user for approval
    questions = {
        "pictures": "Ech sin domat averstanen, dass vu mengem Kand Fotoe gemaach gin.",
        "social_media": "Ech sin domat averstanen, dass Fotoen, déi am Laf vu (Gruppen)Aktivitéiten vu mengem Kand gemach gin, op de soziale Medien (Facebook) vum Käler Scoutsgrupp gedeelt kenne gin.",
        "contact": "Ech sin domat averstanen, dass meng Email Adress an Telefonsnummer benotzt gin, fir vun de Cheffe kontaktéiert ze gin.",
        "home_alone": "Mäi Kand dierf no der Versammlung eleng heem goen."
    }
    
    # Concatenate forms and corresponding submit buttons (see definition in forms.py)
    forms = [form_user, form_tutor, form_urgent, form_questions]
    submit_buttons = ["submit_1", "submit_2", "submit_3", "submit_4"]
    
    if request.method == "POST":
        # Loop through forms
        for form, submit_button in zip(forms, submit_buttons):
            # Check pressed submit button
            if getattr(form, submit_button).data:
                # Check if form is valid
                if form.validate():
                    # Save form data in session
                    session[form.name + "_data"] = form.data
                    print(form.data)
                    
                    # Make list from form data for database insertion
                    session[form.name + "_list"] = list(session[form.name + "_data"].values())
                    print(session[form.name + "_list"])

                    # Format birthday because of unexpected auto-formatting by WTForm (issue #2); also update the list
                    if form.name == "form_user":
                        session["form_user_data"]["birthday"] = session["form_user_data"]["birthday"].strftime("%Y-%m-%d")
                        session["form_user_list"] = list(session["form_user_data"].values())
                    
                    # If last form (i.e empty redirect field)
                    if form.redirect_tab == "":
                        # Connect to database
                        db = get_db()
                        
                        # Add user to user table
                        try:
                            db.execute("INSERT INTO user (first_name, last_name, birthday, gender, number, branch, email, allergies, diet, other_information) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                   (*session["form_user_list"][:10],))
                        except db.IntegrityError:
                            flash("E Feeler ass opgetrueden. Feeler Code 100.")
                        
                        # Get ID of added user
                        user = session["form_user_data"]
                        try:
                            user_id = db.execute("SELECT id FROM user WHERE first_name = ? AND last_name = ? AND birthday = ?", (user["first_name"], user["last_name"], user["birthday"])).fetchone()
                        except db.IntegrityError:
                            flash("E Feeler ass opgetrueden. Feeler Code 101.")

                        # Add address to address table
                        try:
                            db.execute("INSERT INTO address (house_number, street, town, zip, country, user_id) VALUES (?, ?, ?, ?, ?, ?)", (user["house_number"], user["street"].upper(), user["town"].upper(), user["zip"], user["country"], user_id[0]))
                        except db.IntegrityError:
                            flash("E Feeler ass opgetrueden. Feeler Code 102.")

                        # Add first parent to parent table
                        parent = session["form_tutor_data"]
                        # Check if parent exists
                        exists = db.execute("SELECT id FROM parent WHERE phone_number = ? AND email = ?", (parent["number_1"], parent["email_1"])).fetchone()
                        if exists is None:
                            try:
                                db.execute("INSERT INTO parent (first_name, last_name, phone_number, email) VALUES (?, ?, ?, ?)", (parent["first_name_1"].upper(), parent["last_name_1"].upper(), parent["number_1"], parent["email_1"]))
                            except db.IntegrityError:
                                flash("E Feeler ass opgetrueden. Feeler Code 103.")
                        # Get id of first parent
                        try:
                            parent_id_1 = db.execute("SELECT id FROM parent WHERE first_name = ? AND last_name = ? AND phone_number = ? AND email = ?", (parent["first_name_1"].upper(), parent["last_name_1"].upper(), parent["number_1"], parent["email_1"])).fetchone()
                        except db.IntegrityError:
                            flash("E Feeler ass opgetrueden. Feeler Code 104.")
                        # Add emergency contact to emergency table
                        emergency = session["form_urgent_data"]
                        # Check if emergency contact exists
                        exists = db.execute("SELECT id FROM emergency WHERE phone_number = ? AND email = ?", (emergency["number_3"], emergency["email_3"])).fetchone()
                        if exists is None:
                            print("executing")
                            try:
                                db.execute("INSERT INTO emergency (first_name, last_name, phone_number, email) VALUES (?, ?, ?, ?)", (emergency["first_name_3"].upper(), emergency["last_name_3"].upper(), emergency["number_3"], emergency["email_3"]))
                            except db.IntegrityError:
                                flash("E Feeler ass opgetrueden. Feeler Code 105.")
                        # Get id of emergency contact
                        emergency_id = db.execute("SELECT id FROM emergency WHERE first_name = ? AND last_name = ? AND phone_number = ? AND email = ?", (emergency["first_name_3"].upper(), emergency["last_name_3"].upper(), emergency["number_3"], emergency["email_3"])).fetchone()
                        # Link first parent-child-emergency contact
                        try:
                            db.execute("INSERT INTO parent_child_emergency (parent_id, child_id, emergency_id) VALUES (?, ?, ?)", (parent_id_1[0], user_id[0], emergency_id[0]))
                        except db.IntegrityError:
                            flash("E Feeler ass opgetrueden. Feeler Code 106.")
                            
                        # Check if second parent submitted
                        if parent["first_name_2"] != '':
                            # Check if second parent exists
                            exists = db.execute("SELECT id FROM parent WHERE phone_number = ? AND email = ?", (parent["number_2"], parent["email_2"])).fetchone()
                            if exists is None:
                                # Add second parent to parent table
                                try:
                                    db.execute("INSERT INTO parent (first_name, last_name, phone_number, email) VALUES (?, ?, ?, ?)", (parent["first_name_2"].upper(), parent["last_name_2"].upper(), parent["number_2"], parent["email_2"]))
                                except db.IntegrityError:
                                    flash("E Feeler ass opgetrueden. Feeler Code 107.")
                            # Get id of second parent
                            parent_id_2 = db.execute("SELECT id FROM parent WHERE first_name = ? AND last_name = ? AND phone_number = ? AND email = ?", (parent["first_name_2"].upper(), parent["last_name_2"].upper(), parent["number_2"], parent["email_2"])).fetchone()
                            # Link second parent-child-emergency contact
                            try:
                                db.execute("INSERT INTO parent_child (parent_id, child_id, emergency_id) VALUES (?, ?, ?)", (parent_id_2[0], user_id[0], emergency_id[0]))
                            except db.IntegrityError:
                                flash("E Feeler ass opgetrueden. Feeler Code 108.")

                        # Commit database changes
                        db.commit()
                        
                        # Email logic
                        from pandas import DataFrame
                        from openpyxl import Workbook
                        import os
                        
                        msg = Message('Nei Umeldung bei den Wëllefcher', sender='peter@mailtrap.io', recipients=['paul@mailtrap.io'])
                        
                        list_data = session["form_user_list"][:10] + session["form_tutor_list"][:8] + session["form_urgent_list"][:4] + session["form_questions_list"][:4]
                        
                        df = DataFrame([list_data], columns=["Virnumm", "Nonumm", "Gebuertsdatum", "Geschlecht", "Handynummer", "Branche", "Email", "Allergien", "Régime", "Aner Informatiounen", "Virnumm", "Noonumm", "Handynummer", "Email", "Virnumm", "Noonumm", "Handynummer", "Email", "Virnumm", "Noonumm", "Handynummer", "Email", "Fotoen", "Social Media", "Kontakt", "Aleng heem"])

                        # Create temporary xlsx file
                        tmp_xlsx = Workbook()
                        tmp_xlsx.save("flaskr/tmp.xlsx")
                        
                        df.to_excel('flaskr/tmp.xlsx', index=False)
                        
                        from flask import current_app
                        
                        with open("flaskr/tmp.xlsx", "rb") as fp:
                            msg.attach("tmp.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", fp.read())

                        mail.send(msg)
                        
                        # Remove temporary xlsx file
                        os.remove("flaskr/tmp.xlsx")
                        
                        # Clear session information (functional improvement to make: store key name in form class)
                        for key in ["form_user_data", "form_tutor_data", "form_urgent_data"]:
                            session.pop(key, default=None)

                        # Redirect to home page and flash success message
                        flash("Dir gouft ugemellt!")
                        return redirect(url_for("index.index"))
                    
                    # If not last form, redirect to next form
                    else:
                        return render_template("index/apply.html", active_tab = form.redirect_tab, form_user=form_user, form_tutor=form_tutor, form_urgent=form_urgent, form_questions=form_questions, questions=questions, session=session,
                                                                                user_data=session["form_user_data"], tutor_data=session["form_tutor_data"], urgent_data=session["form_urgent_data"])
                
                # invalid form: render same html, populate field entries with data already entered
                else:
                    print(form.name)
                    return render_template("index/apply.html", active_tab=form.tab, form_user=form_user, form_tutor=form_tutor, form_urgent=form_urgent, form_questions=form_questions, questions=questions,
                                                                                    user_data=session["form_user_data"], tutor_data=session["form_tutor_data"], urgent_data=session["form_urgent_data"])
    if request.method == "GET":
        return render_template("index/apply.html", active_tab="form-user", form_questions=form_questions, form_user=form_user, form_tutor=form_tutor, form_urgent=form_urgent, user_data=session["form_user_data"], tutor_data=session["form_tutor_data"], urgent_data=session["form_urgent_data"], questions=questions)