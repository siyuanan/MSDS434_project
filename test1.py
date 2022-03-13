import os
import pandas as pd
from flask import Flask, render_template, request
from google.cloud import bigquery

from test_func import test_func
import main

app = Flask(__name__)

def test1():
    result = test_func()
    assert result == "Test"

def main_test(): 
    main.app.testing = True
    client = main.app.test_client()

    r = client.get('/')
    assert r.status_code == 200
    assert 'Welcome to the new app!' in r.data.decode('utf-8')

@app.route('/data', methods=['GET', 'POST'])
def form():
    form_data = request.form

    return render_template('data.html', form_data = form_data, var_list = ['name', 'country'])


if __name__ == "__main__":
    app.run(host = '127.0.0.1', debug = True, port=int(os.environ.get("PORT", 8080)))