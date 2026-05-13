import requests

BASE_URL = 'http://127.0.0.1:8000'
SESSION_HEADER = 'Bearer ses_12204e901e061f1421834b7bf57b027b56a6870641ea29230eafc11f3aed9f5e'


def test_get_account_list():
    URL = BASE_URL + '/api/v1/account/list/'
    r = requests.get(url=URL, headers={'Authorization': SESSION_HEADER})
    print(r.json())

def test_get_account_transfers():
    URL = BASE_URL + '/api/v1/account/2/transfers/'
    r = requests.get(url=URL, headers={'Authorization': SESSION_HEADER})
    print(r.json())

def test_get_account_transfers_non_owned():
    URL = BASE_URL + '/api/v1/account/1/transfers/'
    r = requests.get(url=URL, headers={'Authorization': SESSION_HEADER})
    print(r.json())

def test_list_accounts_valid_token():
    URL = BASE_URL + '/api/v1/account/list/'
    r = requests.get(url=URL, headers={'Authorization': SESSION_HEADER})
    assert r.status_code == 200, f"Server returned non-200 (Success) response code for valid request: {r.json().get('reason')}"

def test_list_accounts_invalid_token():
    URL = BASE_URL + '/api/v1/account/list/'
    r = requests.get(url=URL, headers={'Authorization': 'ses_invalid_token'})
    assert r.status_code == 404, f"Server returned non-404 (Not Found) response code for valid request."