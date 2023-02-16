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
    token = db.get_token(cur)
    result = db.insert(cur, con, "user", "(name, email, password, creation_date, token)", str((name, email, password, creation_date,token)))
    print(token)
    if result:
        return "true"
    else:
        return "false"

@app.route('/get/list', methods=['POST'])
def get_list():
    idd = request.form['id']
    user = db.fetch(cur, 'user', cond='id = {}'.format(idd))
    print(user)
    if request.form['token'] != user[1]:
        return '0'
    if not user:
        listt = db.fetch(cur, 'list', cond='user = {}'.format(user['id']))
        return jsonify(listt)
    else:
        return '0'
