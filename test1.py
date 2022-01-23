from test_func import test_func
import main

def test1():
    result = test_func()
    assert result == "Test"

def main_test(): 
    main.app.testing = True
    client = main.app.test_client()

    r = client.get('/')
    assert r.status_code == 200
    assert 'Welcome to the new app!' in r.data.decode('utf-8')
