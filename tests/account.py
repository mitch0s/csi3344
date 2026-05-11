import requests

BASE_URL = 'http://127.0.0.1:8000'

def test_get_account_list():
    URL = BASE_URL + '/api/v1/account/list/'
    r = requests.get(url=URL, headers={}, json={'session_token': 'ses_123123123'})
    print(r.json())



def main():
    test_get_account_list()

if __name__ == '__main__':
    main()