#!/usr/bin/env python3
from flask import *
import DBconnect as db
import hashlib
import time
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required
from datetime import timedelta

app = Blueprint('api_recieve', __name__)
con = db.conn()

@app.route('/login', methods=['POST'])
def login():
    login = request.form['email']
    password = hashlib.sha256(request.form['password'].encode()).hexdigest()
    result = db.fetch("user", "email = '{}' AND password = '{}'".format(login, password))
    access_token = create_access_token(identity=login)
    if result != None:
        return jsonify(access_token=access_token)
    else:
        return jsonify("Wrong username or password"), 401

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = hashlib.sha256(request.form['password'].encode()).hexdigest()
    name = request.form['name']
    creation_date = time.strftime('%Y-%m-%d %H:%M:%S')
    token = db.get_token(email)
    result = db.insert("user", "(name, email, password, creation_date, token)", str((name, email, password, creation_date,token)))
    print(token)
    if result:
        return "Access registration",200
    else:
        return jsonify("Wrong username or password"), 401

@app.route('/get/list', methods=['POST'])
@jwt_required()
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

@app.route('/create/task', methods=['POST'])
def create_task():
    keys = "(name, list, creation_date"
    id = request.form["id"]
    token = create_access_token(identity = id,expires_delta=24)
    name = request.form["name"]
    creation_date = time.strftime('%Y-%m-%d %H:%M:%S')
    listt = request.form["list"]
    value = [name, listt, creation_date]
    if "task" in request.form:
        task = request.form["task"]
        keys += ", task"
        value.append(task)
    if "content" in request.form:
        content = request.form["content"]
        keys += ", content"
        value.append(content)
    if "deadline" in request.form:
        deadline = request.form["deadline"]
        keys += ", deadline"
        value.append(deadline)
    keys += ")"
    return db.insert("task", keys, str(list(value)))
