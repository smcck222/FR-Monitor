import flask
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/dashboard', methods=["POST"])
def receive_alert(): 
    content = request.json
    print(content['login_name'] + " " + content['type'])

    return("server running")

@app.route('/')
def index(): 

    return("SERVER DASHBOARD RUNNING")

if __name__ == "__main__":
    app.run(debug = True)


