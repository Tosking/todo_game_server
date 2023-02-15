#!/usr/bin/env python3
from flask import *
import DBconnect as db
import hashlib

app = Blueprint('api_recieve', __name__)
cur, con = db.conn()

@app.route('/login', methods=['POST'])
def login():
    login = request.form['login']
    password = hashlib.sha256(request.form['password'].encode()).hexdigest()
    result = db.fetch(cur, "user", "email = '{}' AND password = '{}'".format(login, password))
    if result != None:
        return "true"
    else:
        return "false"
