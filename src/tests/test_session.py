import requests

BASE_URL = 'http://127.0.0.1:8000'
SESSION_HEADER = 'Bearer ses_12204e901e061f1421834b7bf57b027b56a6870641ea29230eafc11f3aed9f5e'

def test_create_session_valid_base_case():
    URL = BASE_URL + '/api/v1/user/session/'
    r = requests.post(
        url=URL, 
        headers={}, 
        json={'email_address': 'mitch@neutron.au', 'password': 'test123'}
    )
    assert r.status_code == 200, f"Endpoint failed to create session:{r.json().get('reason')}"

def test_create_session_create_invalid_email():
    URL = BASE_URL + '/api/v1/user/session/'
    r = requests.post(
        url=URL, 
        headers={}, 
        json={'email_address': 'mitch@commonsystems.com.au', 'password': 'test123'}
    )
    assert r.status_code != 200, "Endpoint created session despite supply of invalid account email address."

def test_create_session_create_invalid_password():
    URL = BASE_URL + '/api/v1/user/session/'
    r = requests.post(
        url=URL, 
        headers={}, 
        json={'email_address': 'mitch@neutron.au', 'password': 'invalid_password_123'}
    )
    assert r.status_code != 200, "Endpoint created session despite supply of invalid account password."
