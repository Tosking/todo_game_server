#!/usr/bin/env python3
from flask import *
import DBconnect as db
import hashlib
import time
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required
from datetime import timedelta
import re

app = Blueprint('api_recieve', __name__)
con = db.conn()

'''
TODO:
1)удаление листа
2)удаление задачи
3)получение задачи
'''

def trim(s):
    re.sub(r'/[^a-z\d\-\s]/gi', '', s)
    re.sub(r'/^[^a-z\d]+/i', '', s)
    re.sub(r'/[^a-z\d]+$/i', '', s)
    return s

@app.route('/login', methods=['POST'])
def login():
    login = request.form['email']
    password = hashlib.sha256(request.form['password'].encode()).hexdigest()
    result = db.fetch("user", "email = '{}' AND password = '{}'".format(login, password))
    access_token =db.get_token(login)
    if result != None:
        return jsonify(access_token=access_token)
    else:
        return jsonify("Wrong username or password"), 401

@app.route('/register', methods=['POST'])
def register():
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    email = request.form['email']
    if not re.fullmatch(regex, email):
        return '400'
    password = hashlib.sha256(request.form['password'].encode()).hexdigest()
    name = request.form['name']
    name = trim(name)
    print("Name:",name)
    creation_date = time.strftime('%Y-%m-%d %H:%M:%S')
    access_token = db.get_token(email)
    result = db.insert("user", "(name, email, password, creation_date, token)", str((name, email, password, creation_date,access_token)))
    print(access_token)
    if result:
        return "Access registration",200
    else:
        return jsonify("Wrong username or password"), 401

@app.route('/get/list', methods=['POST'])
@jwt_required()
def get_list():
    login = get_jwt_identity()
    idd = request.form['id']
    user = db.fetch('user', cond='id = {}'.format(idd))
    if(login !=user[3]):
        return "Wrong!",400
    print("User:",user)
    if user:
        if request.form['token'] != user[1]:
            return '2'
        listt = db.fetch('list', cond='user = {}'.format(user[0]))
        if listt:
            return jsonify(listt)
        else:
            return '0'

@app.route('/create/list', methods=['POST'])
@jwt_required()
def create_list():
    login = get_jwt_identity()
    idd = request.form['id']
    user = db.fetch('user', cond='id = {}'.format(idd))
    print(user)
    if user:
        if(login !=user[3]):
            return "Wrong!",400
        name = request.form['name']
        name = trim(name)
        if name == "":
            return '400'
        creation_date = time.strftime('%Y-%m-%d %H:%M:%S')
        result = db.insert('list', '(name, creation_date, user)', str((name, creation_date, idd)))
        return str(result)
    else:
        return "502"
    
@app.route('/delete/list', methods=['POST'])
@jwt_required()
def delete_list():
    login = get_jwt_identity()
    idd = request.form['id']
    name = request.form['name']
    user = db.fetch('user', cond='id = {}'.format(idd))
    lists = db.fetch('list',cond="user = {} AND name = '{}'".format(idd,name))
    if user and lists:
        if(login !=user[3]):
            return "Wrong!",400
        name = trim(name)
        if name == "":
            return '400'
        result = db.delete('list', cond="user = {} AND name = '{}'".format(idd,name))
        return "List is deleted successfully",200
    else:
        return "Bad gateway",502
    
@app.route('/create/task', methods=['POST'])
@jwt_required()
def create_task():
    login = get_jwt_identity()
    user = db.fetch('user', cond='id = {}'.format(request.form['id']))
    if not user and login != user[3]:
        return "Wrong!",400
    keys = "(name, list, creation_date"
    id = request.form["id"]
    token = create_access_token(identity = id,expires_delta=24)
    name = request.form["name"]
    name = trim(name)
    if name == "":
        return '400'
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
'''

@app.route('/delete/task', methods=['POST'])
@jwt_required()
def delete_task():
    None

@app.route('/get/task', methods=['POST'])
@jwt_required()
def delete_list():
    None
'''
