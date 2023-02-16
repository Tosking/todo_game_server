#!/usr/bin/env python3
from flask import *
import DBconnect as db
import hashlib
import time

app = Blueprint('api_recieve', __name__)
cur, con = db.conn()
@app.route('/login', methods=['POST'])
def login():
    login = request.form['email']
    password = hashlib.sha256(request.form['password'].encode()).hexdigest()
    result = db.fetch(cur, "user", "email = '{}' AND password = '{}'".format(login, password))
    if result != None:
        return "true"
    else:
        return "false"

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = hashlib.sha256(request.form['password'].encode()).hexdigest()
    name = request.form['name']
    creation_date = time.strftime('%Y-%m-%d %H:%M:%S')
    result = db.insert(cur, con, "user", "(name, email, password, creation_date)", str((name, email, password, creation_date)))
    token = db.get_token(cur)
    print(token)
    if result:
        return "true"
    else:
        return "false"
