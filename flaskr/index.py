import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint("index", __name__)

# This BP should handle ALL the routes that should be accessible to anyone, not only those with an account


@bp.route("/")
def index():
    # A test, I will have to create an html file that EXTENDS base.html to show actual content on the website
    return render_template("index/index.html")

@bp.route("/apply")
def apply():
    
    # Questions on form
    questions = {}
    questions[1] = "Ech sin domat averstanen, dass vu mengem Kand Fotoe gemaach gin."
    questions[2] = "Ech sin domat averstanen, dass Fotoen, déi am Laf vu (Gruppen)Aktivitéiten vu mengem Kand gemach goufen, op de soziale Medien (Facebook) vum Käler Scoutsgrupp gedeelt kenne gin."
    questions[3] = "Ech sin domat averstanen, dass meng Email Adress an Telefonsnummer benotzt gin, fir vun de Cheffe kontaktéiert ze gin."
    questions[4] = "Mäi Kand dierf no der Versammlung eleng heem goen."
    
    return render_template("index/apply.html", questions=questions)

@bp.route("/contact")
def contact():
    return render_template("index/contact.html")
