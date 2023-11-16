import pytest
from flask import g, session
from flaskr.db import get_db
        
# test account view if user not logged in
def test_account_unlogged(client):
    assert client.get('/auth/account').status_code == 302
    
# test account view if user logged in
def test_account_unlogged(client, auth):
    auth.login()
    
    assert client.get('/auth/account').status_code == 200