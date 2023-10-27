# This file contains setup functions ("fixtures") that EACH test will use
# Fixture will call the factory and pass test_config to to configure the app and database for testing
# From https://flask.palletsprojects.com/en/3.0.x/tutorial/tests/

import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')
    
@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app({
    'TESTING': True,
    'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)
    
@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# define Python class, inherits from base `object` class
class AuthActions(object):
    # constructor method
    def __init__(self, client):
        self._client = client

    def login(self, username='johndoe', password='test'):
        # send post request to login with username and password equal to a; return the reponse
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    # return object of class AuthActions with client argument
    return AuthActions(client)