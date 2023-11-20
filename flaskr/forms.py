from flask_wtf import FlaskForm
import email_validator
# Import fields required for form
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField, SelectField, EmailField, DateField, SubmitField)
# Import validators
from wtforms.validators import InputRequired, Length, Email, Optional
class ScoutForm(FlaskForm):
    # Details
    first_name = StringField('Virnumm', validators=[InputRequired()])
    last_name = StringField('Numm', validators=[InputRequired()])
    birthday = DateField('Gebuertsdatum')
    gender = RadioField('Geschlecht', choices=['Weiblech', 'Männlech'])
    number = IntegerField('Handynummer', validators=[Optional(strip_whitespace=True)])
    branch = SelectField('Branche', choices=['Wëllefcher'], default='Wëllefcher')
    email = EmailField('Email')
    allergies = StringField('Ech hun Allergien op ...')
    diet = StringField('Ech hun e speziellen Régime ...')
    other = TextAreaField('Aner Informatiounen iwwert mech ...')
    
    # Address
    house_number = StringField('Hausnummer', validators=[InputRequired()])
    street = StringField('Strooss', validators=[InputRequired()])
    town = StringField('Uertschaft', validators=[InputRequired()])
    zip = IntegerField('Postleitzuel', validators=[InputRequired()])
    country = SelectField('Land', choices=['Lëtzebuerg', 'Belgique', 'France', 'Deutschland'], default='Lëtzebuerg', validators=[InputRequired()])
    
    # Submit button
    submit_1 = SubmitField("Weider")
    
    # Field names
    field_names_scout = ["first_name", "last_name", "birthday", "gender", "number", "branch", "email", "house_number", "street", "town", "zip", "country", "allergies", "diet", "other"]
    
    # Form name and redirect tab
    name = "form_user"
    redirect_tab = "form_tutor"
    
class TutorForm(FlaskForm):
    # First tutor
    first_name_1 = StringField('Virnumm', validators=[InputRequired()])
    last_name_1 = StringField('Numm', validators=[InputRequired()])
    number_1 = StringField('Handynummer', validators=[InputRequired()])
    email_1 = EmailField('Email', validators=[InputRequired(), Email()])
    
    # Second tutor
    first_name_2 = StringField('Virnumm')
    last_name_2 = StringField('Numm')
    number_2 = StringField('Handynummer')
    email_2 = EmailField('Email')
    
    # Submit button
    submit_2 = SubmitField("Weider")
    
    # Field names
    field_names_tutor_1 = ["first_name_1", "last_name_1", "number_1", "email_1"]
    field_names_tutor_2 = ["first_name_2", "last_name_2", "number_2", "email_2"]
    
    # Form name and redirect tab
    name = "form_tutor"
    redirect_tab = "form_emergency"
    
class EmergencyForm(FlaskForm):
    # Emergency contact
    first_name_3 = StringField('Virnumm', validators=[InputRequired()])
    last_name_3 = StringField('Numm', validators=[InputRequired()])
    number_3 = StringField('Handynummer', validators=[InputRequired()])
    email_3 = EmailField('Email', validators=[InputRequired(), Email()])
    
    # Submit button
    submit_3 = SubmitField("Weider")
    
    # Field names
    field_names_emergency = ["first_name_3", "last_name_3", "number_3", "email_3"]
    
    # Form name and redirect tab
    name = "form_emergency"
    redirect_tab = "form_questions"
    
class QuestionsForm(FlaskForm):
    # Questions
    pictures = BooleanField("Pictures")
    social_media = BooleanField("Social Media")
    contact = BooleanField("Contact")
    home_alone = BooleanField("Home Alone")
    
    # Submit button
    submit_4 = SubmitField("Umellen")
    
    # Field names
    field_names_questions = ["pictures", "social_media", "contact", "home_alone"]
    
    # Form name and redirect tab
    name = "form_questions"
    redirect_tab = ""

    

    
    
