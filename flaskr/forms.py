from flask_wtf import FlaskForm

import email_validator

# Import fields required for form
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField, SelectField, EmailField, DateField, SubmitField)


# Import validators
from wtforms.validators import InputRequired, Length, Email


class userForm(FlaskForm):
    # Child
    first_name = StringField('Virnumm', validators=[InputRequired()])
    last_name = StringField('Numm', validators=[InputRequired()])
    birthday = DateField('Gebuertsdatum')
    gender = RadioField('Geschlecht', choices=["Weiblech", "Männlech"])
    number = IntegerField('Handynummer', validators=[InputRequired()])
    branch = SelectField("Branche", choices=["Wëllefcher"], default="Wëllefcher")
    email = EmailField('Email')
    
    house_number = StringField('Hausnummer', validators=[InputRequired()])
    street = StringField('Strooss', validators=[InputRequired()])
    town = StringField('Uertschaft', validators=[InputRequired()])
    zip = IntegerField('Postleitzuel', validators=[InputRequired()])
    country = SelectField('Land', choices=["Luxembourg", "Belgique", "France", "Deutschland"], default="Luxembourg", validators=[InputRequired()])
    
    allergies = StringField("Ech hun Allergien op ...")
    diet = StringField("Ech hun e speziellen Régime ...")
    other_information = TextAreaField("Aner Informatiounen iwwert mech ...")
    
    submit_1 = SubmitField("Weider")
    
    tab = "form-user"
    name = "form_user"
    redirect_tab = "form-tutor"
    
class tutorForm(FlaskForm):
    first_name_1 = StringField('Virnumm', validators=[InputRequired()])
    last_name_1 = StringField('Numm', validators=[InputRequired()])
    number_1 = StringField('Handynummer', validators=[InputRequired()])
    email_1 = EmailField('Email', validators=[InputRequired(), Email()])
    
    first_name_2 = StringField('Virnumm')
    last_name_2 = StringField('Numm')
    number_2 = StringField('Handynummer')
    email_2 = EmailField('Email')
    
    submit_2 = SubmitField("Weider")
    
    tab = "form-tutor"
    name = "form_tutor"
    redirect_tab = "form-urgent"
    
class urgentForm(FlaskForm):
    first_name_3 = StringField('Virnumm', validators=[InputRequired()])
    last_name_3 = StringField('Numm', validators=[InputRequired()])
    number_3 = StringField('Handynummer', validators=[InputRequired()])
    email_3 = EmailField('Email', validators=[InputRequired(), Email()])
    
    submit_3 = SubmitField("Weider")
    
    tab = "form-urgent"
    name = "form_urgent"
    redirect_tab = "form-questions"
    
class questionsForm(FlaskForm):
    pictures = BooleanField("Pictures")
    social_media = BooleanField("Social Media")
    contact = BooleanField("Contact")
    home_alone = BooleanField("Home Alone")
    
    submit_4 = SubmitField("Umellen")
    
    tab = "form-questions"
    name = "form_questions"
    redirect_tab = ""

    

    
    
