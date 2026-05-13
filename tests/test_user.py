import requests

BASE_URL = 'http://127.0.0.1:8000'
SESSION_HEADER = 'Bearer ses_Y7VBFw0taJGjs6cqfxVKKtvSTgxdIKamugv92MUIhGRYPAKcEML5d82QZokFp1se'

def test_get_user_missing_headers():
    URL = BASE_URL + '/api/v1/user/'
    r = requests.get(url=URL, headers={})
    assert r.status_code == 404, "Server returned non-404 (Bad Request) response code for missing headers"

def test_get_user_valid_token():
    URL = BASE_URL + '/api/v1/user/'
    r = requests.get(url=URL, headers={'Authorization': SESSION_HEADER})
    assert r.status_code == 200, f"Server returned non-200 (Success) response code for valid request: {r.json().get('reason')}"

def test_get_user_invalid_token():
    URL = BASE_URL + '/api/v1/user/'
    r = requests.get(url=URL, headers={'Authorization': 'ses_invalid_token'})
    assert r.status_code != 200, f"Server 200 (Success) response code for request containing invalid token"
