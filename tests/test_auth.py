import pytest
from flask import g, session
from flaskr.db import get_db

# test register
def test_register(client, app):
    # check GET
    assert client.get('/auth/register').status_code == 200
    
    # check POST
    response = client.post(
        '/auth/register', data={'first_name': 'a',
                                'last_name': 'a',
                                'username': 'a',
                                'password': 'a',
                                'passwordConfirm': 'a',
                                'birthday': '1997-01-25',
                                'gender': 'a',
                                'house_number': 'a',
                                'street': 'a',
                                'town': 'a',
                                'country': 'a',
                                'zip': '5',
                                'conditionsCheck': 'a'}
    )
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None

# pass invalid arguments and check if correct message printed
@pytest.mark.parametrize(('first_name', 'last_name', 'username', 'password', 'passwordConfirm', 'birthday', 'gender', 'house_number', 'street', 'town', 'country', 'zip', 'conditionsCheck', 'message'), 
                         (('a', 'a', 'a', 'a', 'b', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', b'Dir hudd zwee verschidden Passwieder agin.'),
))
def test_register_validate_input(client, first_name, last_name, username, password, passwordConfirm, birthday, gender, house_number, street, town, country, zip, conditionsCheck, message):
    response = client.post(
        '/auth/register',
        data={'first_name': first_name, 'last_name': last_name, 'username': username,
              'password': password, 'passwordConfirm': passwordConfirm, 'birthday': birthday,
              'gender': gender, 'house_number': house_number, 'street': street, 'town': town,
              'country': country, 'zip': zip, 'conditionsCheck': conditionsCheck, 'message': message}
    )
    assert message in response.data
    
# test login
def test_login(client, auth):
    # Check get
    assert client.get('/auth/login').status_code == 200

    # login with username = 'test' and password = 'test'
    response = auth.login()
    
    # check correct redirect to home
    #assert response.headers["Location"] == ""

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'johndoe'


# test logout
def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
        
# test account view if user not logged in
def test_account_unlogged(client):
    assert client.get('/auth/account').status_code == 302
    
# test account view if user logged in
def test_account_unlogged(client, auth):
    auth.login()
    
    assert client.get('/auth/account').status_code == 200