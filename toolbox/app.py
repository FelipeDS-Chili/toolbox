from flask import Flask, escape, request

import pandas as pandas
import joblib


app = Flask(__name__)

@app.route('/')
def hello():
    name = rquest.args.get('name', 'World')
    return f'Hello, {name}!'
