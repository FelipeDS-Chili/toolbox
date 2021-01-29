from flask import Flask, escape, request, render_template

import pandas as pandas



app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.html')

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port =5000, debug=True)

