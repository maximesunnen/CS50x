import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

from flaskr.auth import login_required

from .helpers.form_helpers import form_filled_in

from flaskr.forms import userForm, tutorForm, urgentForm, questionsForm

from .mail import mail

from flask_mail import Message

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

def apply():
    # instantiate CourseForm() class; save instance in `form`
    form = CourseForm()
    
    # validate_on_submit checks for POST request
    if form.validate_on_submit():
        
        # Connect to database
        db = get_db()
        
        # Add user to database
        try:
            db.execute("INSERT INTO user (first_name, last_name, birthday, gender, allergies, diet, branch, other_information) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (form.first_name.data.strip().upper(), form.last_name.data.strip().upper(), form.birthday.data, 
                        form.gender.data.strip().upper(), form.allergies.data, form.diet.data, 
                        form.branch.data.strip().upper(), form.other_information.data))
        except db.IntegrityError:
            flash("Feeler Code 100")
            return redirect(url_for("index.index"))
        
        db.commit()
        
        # Send email with new application
        from pandas import DataFrame
        
        msg = Message('Nei Umeldung bei den Wëllefcher', sender =   'peter@mailtrap.io', recipients = ['paul@mailtrap.io'])
        
        data = DataFrame([form.data])

        data.to_csv('flaskr/test.csv', index=False, encoding="utf-8")
        
        from flask import current_app
        
        with current_app.open_resource("test.csv") as fp:
            msg.attach("test.csv", "text/csv", fp.read())
            
        mail.send(msg)
        
        return "Message sent!"
        
        # Redirect and flash message
        flash("Dir gouft ugemellt!")
        return redirect(url_for("index.index"))
    
    return render_template("index/wtforms-test.html", form=form)

@bp.route("/contact", methods=["GET", "POST"])
def contact():
    # Initialize session data
    for session_name in ["form_user_data", "form_tutor_data", "form_urgent_data"]:
        if session.get(session_name) is None:
            session[session_name] = {}

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
    
    # Concatenate forms and corresponding submit buttons (as defined in forms.py)
    forms = [form_user, form_tutor, form_urgent, form_questions]
    submit_buttons = ["submit_1", "submit_2", "submit_3", "submit_4"]
    
    # Post request logic
    if request.method == "POST":
        for form, submit_button in zip(forms, submit_buttons):
            # Check which submit button has been pressed
            if getattr(form, submit_button).data:
                # Check if form is valid
                if form.validate():
                    print("Valid form")
                    print(form.name + "_data")
                    session[form.name + "_data"] = form.data
                    print(session[form.name + "_data"])
                    # Check if the valid form is the last one (i.e empty redirect field)
                    if form.redirect_tab == "":
                        # Database logic
                        
                        # Commit database changes
                        
                        # Email logic
                        
                        # Clear session information (functional improvement to make: store this info in the form classes)
                        for key in ["form_user_data", "form_tutor_data", "form_urgent_data"]:
                            session.pop(key, default=None)
                            
                        # Redirect to home page and flash success message
                        return redirect(url_for("index.index"))
                    # If not last form, redirect to next
                    else:
                        return render_template("index/test.html", active_tab = form.redirect_tab, form_user=form_user, form_tutor=form_tutor, form_urgent=form_urgent, form_questions=form_questions, questions=questions,
                                                                                user_data=session["form_user_data"], tutor_data=session["form_tutor_data"], urgent_data=session["form_urgent_data"])
                
                # if form invalid, render same html but fill in fields with data that has already been entered
                else:
                    print(form.name)
                    return render_template("index/test.html", active_tab=form.tab, form_user=form_user, form_tutor=form_tutor, form_urgent=form_urgent, form_questions=form_questions, questions=questions,
                                                                                    user_data=session["form_user_data"], tutor_data=session["form_tutor_data"], urgent_data=session["form_urgent_data"])
                
                    
    """ if request.method == "POST":
        if form_user.submit_1.data:
            if form_user.validate():
                session["user_data"] = form_user.data
                return render_template("index/test.html", active_tab="form-tutor", form_user=form_user, form_tutor=form_tutor, form_urgent=form_urgent, 
                                                                                    user_data=session["user_data"], tutor_data=session["tutor_data"], urgent_data=session["urgent_data"])
            else:
                return render_template("index/test.html", active_tab="form-user", form_user=form_user, form_tutor=form_tutor, form_urgent=form_urgent, user_data=session["user_data"], tutor_data=session["tutor_data"], urgent_data=session["urgent_data"])
        
        if form_tutor.submit_2.data:
            if form_tutor.validate():
                session["tutor_data"] = form_tutor.data
                return render_template("index/test.html", active_tab="form-urgent", form_user=form_user, form_tutor=form_tutor, form_urgent=form_urgent,
                                                                                    user_data=session["user_data"], tutor_data=session["tutor_data"], urgent_data=session["urgent_data"])
            else:
                return render_template("index/test.html", active_tab="form-tutor", form_user=form_user, form_tutor=form_tutor, form_urgent=form_urgent,
                                                                                    user_data=session["user_data"], tutor_data=session["tutor_data"], urgent_data=session["urgent_data"])
            
        if form_urgent.submit_3.data:
            if form_urgent.validate():
                session["urgent_data"] = form_urgent.data
                return redirect(url_for("index.index"))
            else:
                return render_template("index/test.html", active_tab="form-urgent", form_user=form_user, form_tutor=form_tutor, form_urgent=form_urgent, 
                                                                                    user_data=session["user_data"], tutor_data=session["tutor_data"], urgent_data=session["urgent_data"])
                 """
    if request.method == "GET":
        return render_template("index/test.html", active_tab="form-user", form_questions=form_questions, form_user=form_user, form_tutor=form_tutor, form_urgent=form_urgent, user_data=session["form_user_data"], tutor_data=session["form_tutor_data"], urgent_data=session["form_urgent_data"], questions=questions)