import requests

BASE_URL = 'http://127.0.0.1:8000'

def test_get_user_missing_body():
    URL = BASE_URL + '/api/v1/user/'
    r = requests.get(url=URL, headers={}, json={'sessio_token': 'qwertyop123'})
    print(r.json())

def test_get_user_invalid_token():
    URL = BASE_URL + '/api/v1/user/'
    r = requests.get(url=URL, headers={}, json={'session_token': 'qwertyop123'})
    print(r.json())

def test_get_user_valid_token():
    URL = BASE_URL + '/api/v1/user/'
    r = requests.get(url=URL, headers={}, json={'session_token': 'ses_123123123'})
    print(r.json())

def main():
    test_get_user_missing_body()
    test_get_user_invalid_token()
    test_get_user_valid_token()

if __name__ == '__main__':
    main()