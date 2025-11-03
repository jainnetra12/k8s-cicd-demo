# app.py
from flask import Flask, os

app = Flask(__name__)
# Get the environment where we are running (test or production)
ENVIRONMENT = os.environ.get('K8S_ENV', 'development') 

@app.route('/')
def status():
    return f'<h1>Student Dashboard: Running in {ENVIRONMENT} Environment</h1>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)