# File contains the application factory && tells Python that flaskr is a "package"

import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db
    db.init_app(app)
    
    # Register auth blueprint
    """ from . import auth  # this command EXECUTES code inside auth.py
    app.register_blueprint(auth.bp) """
    
    # Register index blueprint
    from . import index
    app.register_blueprint(index.bp)
    app.add_url_rule('/', endpoint='index')
    
    from . import forms
    
    
    # Flask-Mail configuration
    import socket

    import configparser

    config = configparser.ConfigParser()
    config.read('flaskr/config.ini')

    app.config['MAIL_SERVER'] = config.get('DEFAULT', 'MAIL_SERVER')
    app.config['MAIL_PORT'] = config.getint('DEFAULT', 'MAIL_PORT')
    app.config['MAIL_USERNAME'] = config.get('DEFAULT', 'MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = config.get('DEFAULT', 'MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = config.getboolean('DEFAULT', 'MAIL_USE_TLS', fallback=True)
    app.config['MAIL_USE_SSL'] = config.getboolean('DEFAULT', 'MAIL_USE_SSL', fallback=False)

    # import mail from mail.py
    from .mail import mail
    mail.init_app(app)
    
    # Add simple route for testing
    @app.route('/test')
    def test():
        return "Test"

    return app