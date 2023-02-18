#!/usr/bin/env python3
from flask import *
import DBconnect as db
import hashlib
import time

app = Blueprint('api_recieve', __name__)
con = db.conn()
@app.route('/login', methods=['POST'])
def login():
    login = request.form['email']
    password = hashlib.sha256(request.form['password'].encode()).hexdigest()
    result = db.fetch("user", "email = '{}' AND password = '{}'".format(login, password))
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
    token = db.get_token()
    result = db.insert("user", "(name, email, password, creation_date, token)", str((name, email, password, creation_date,token)))
    print(token)
    if result:
        return "true"
    else:
        return "false"

@app.route('/get/list', methods=['POST'])
def get_list():
    idd = request.form['id']
    user = db.fetch('user', cond='id = {}'.format(idd))
    print(user)
    if user:
        if request.form['token'] != user[1]:
            return '2'
        listt = db.fetch('list', cond='user = {}'.format(user[0]))
        if listt:
            return jsonify(listt)
        else:
            return '0'

@app.route('/create/list', methods=['POST'])
def create_list():
    idd = request.form['id']
    user = db.fetch('user', cond='id = {}'.format(idd))
    print(user)
    if user:
        if request.form['token'] != user[1]:
            return '2'
        name = request.form['name']
        creation_date = time.strftime('%Y-%m-%d %H:%M:%S')
        result = db.insert('list', '(name, creation_date, user)', str((name, creation_date, idd)))
        return str(result)
    else:
        return "2"
