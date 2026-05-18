import requests
import json

BASE_URL = 'http://127.0.0.1:8000'
SESSION_HEADER = 'Bearer ses_iCMFXreWQ0BlLTxXmmWXWJMIHQIJMtG1R5qg1fnK8RcsE9fBTuYOywlb2xVx8PNZ'


def test_get_account_list():
    URL = BASE_URL + '/api/v1/account/list/'
    r = requests.get(url=URL, headers={'Authorization': SESSION_HEADER})
    assert r.status_code == 200, f"Server 200 (Success) response code for request containing invalid token"

def test_get_account_transfers():
    URL = BASE_URL + '/api/v1/account/2/transfers/'
    r = requests.get(url=URL, headers={'Authorization': SESSION_HEADER})
    with open('out.json', 'w+') as file:
        file.write(json.dumps(r.json(), indent=4))
    assert r.status_code == 200, f"Server returned non-200 (Success) response code for valid request: {r.json().get('reason')}"

def test_get_account_transferon_owned():
    URL = BASE_URL + '/api/v1/account/1/transfers/'
    r = requests.get(url=URL, headers={'Authorization': SESSION_HEADER})
    assert r.status_code == 404, f"Server returned non-404 (Not Found) response code for valid request: {r.json().get('reason')}"

def test_list_accounts_valid_token():
    URL = BASE_URL + '/api/v1/account/list/'
    r = requests.get(url=URL, headers={'Authorization': SESSION_HEADER})
    assert r.status_code == 200, f"Server returned non-200 (Success) response code for valid request: {r.json().get('reason')}"

def test_list_accounts_invalid_token():
    URL = BASE_URL + '/api/v1/account/list/'
    r = requests.get(url=URL, headers={'Authorization': 'ses_invalid_token'})
    assert r.status_code == 404, f"Server returned non-404 (Not Found) response code for valid request."