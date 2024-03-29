#!/usr/bin/env python3
from DBconnect import DataBaseConnect
import hashlib
import time
import re
from flask_jwt_extended import get_jwt_identity,jwt_required
from flask import *
from flask_cors import cross_origin


app = Blueprint('api_recieve', __name__)
db = DataBaseConnect()
user_id = 0
data = None

def trim(s):
    re.sub(r'/[^a-z\d\-\s]/gi', '', s)
    re.sub(r'/^[^a-z\d]+/i', '', s)
    re.sub(r'/[^a-z\d]+$/i', '', s)
    return s


@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    data = request.get_json()
    login = data['email']
    if len(str(data['password'])) == 0 or len(str(data['email'])) ==0:
        return jsonify("Wrong, username or password is empty"), 401
    password = hashlib.sha256(data['password'].encode()).hexdigest()
    result = db.fetch("user", "email = '{}' AND password = '{}'".format(login, password))
    access_token =db.get_token(login)
    print(result)
    if result != None and result != False:
        print(jsonify(access_token=access_token))
        return jsonify(access_token=access_token, id=result[0])
    else:
        return jsonify("Wrong username or password"), 401

@app.route('/register', methods=['POST'])
@cross_origin()
def register():
    data = request.get_json()
    name = data['name']
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    email = data['email']
    if len(str(data['password'])) == 0 or len(str(data['email'])) == 0 or len(str(data['name'])) == 0:
        return jsonify("Incorrect input data!"), 401
    if not re.fullmatch(regex, email):
        return '400'
    password = hashlib.sha256(data['password'].encode()).hexdigest()
    name = trim(name)
    creation_date = time.strftime('%Y-%m-%d %H:%M:%S')
    access_token = db.get_token(email)
    result = db.insert("user", "(name, email, password, creation_date, token)", str((name, email, password, creation_date,access_token)))
    if result:
        result = db.fetch("user", "email = '{}' AND password = '{}'".format(email, password))
        return jsonify(access_token=access_token, id=result[0])
    else:
        return jsonify("Wrong username or password"), 401

@app.route('/get/list', methods=['POST'])
@cross_origin()
@jwt_required()
def get_list():
    data = request.get_json()
    login = get_jwt_identity()
    idd = data['id']
    user = db.fetch('user', cond='id = {}'.format(idd))
    if db.verify_token(login, idd):
        return "Wrong!", 400
    if data['token'] != user[1]:
        return '2'
    listt = db.fetch('list', cond='user = {}'.format(user[0]))
    if listt:
        return jsonify(listt)
    else:
        return '0'

@app.route('/create/list', methods=['POST'])
@cross_origin()
@jwt_required()
def create_list():
    data = request.get_json()
    login = get_jwt_identity()
    idd = data['id']
    user = db.fetch('user', cond='id = {}'.format(idd))
    print(user)
    if user:
        if db.verify_token(login, data["id"]):
            return "Wrong!", 400
        name = data['name']
        name = trim(name)
        if name == "":
            return '400'
        creation_date = time.strftime('%Y-%m-%d %H:%M:%S')
        result = db.insert('list', '(name, creation_date, user)', str((name, creation_date, idd)))
        return str(result)
    else:
        return "Bad gateway",502
    
@app.route('/delete/list', methods=['POST'])
@cross_origin()
@jwt_required()
def delete_list():
    data = request.get_json()
    login = get_jwt_identity()
    idd = data['id']
    name = data['name']
    user = db.fetch('user', cond='id = {}'.format(idd))
    lists = db.fetch('list',cond="user = {} AND name = '{}'".format(idd,name))
    if user and lists:
        if db.verify_token(login, data["id"]):
            return "Wrong!", 400
        name = trim(name)
        if name == "":
            return '400'
        result = db.delete('list', cond="user = {} AND name = '{}'".format(idd,name))
        if result:
            return "List is deleted successfully",200
    return "Bad gateway",502

@app.route('/change/email', methods=['POST'])
@cross_origin()
@jwt_required()
def change_email():
    data = request.get_json()
    login = str(get_jwt_identity())
    newuseremail = data['email']
    user = db.fetch(table ='user', cond='email = "{}"'.format(login))
    if db.verify_token(get_jwt_identity(), data["id"]):
        return "Wrong!", 400
    else:
        result = db.update(table='user',sett='`email` = "{}"'.format(newuseremail),cond = '`email` = "{}"'.format(login))
        if result:
            access_token =db.get_token(newuseremail)
            return jsonify(access_token=access_token),200
        else:
            return "Bad gateway",502

@app.route('/change/name', methods=['POST'])
@cross_origin()
@jwt_required()
def change_name():
    data = request.get_json()
    if db.verify_token(get_jwt_identity(), data["id"]):
        return "Wrong!", 400
    login = str(get_jwt_identity())
    newname = data['name']
    user = db.fetch(table ='user', cond='email = "{}"'.format(login))
    print(user)
    if not user:
        return "Wrong!",400
    else:
        result = db.update(table='user',sett='`name` = "{}"'.format(newname),cond = '`email` = "{}"'.format(login))
        if result:
            return "Success",200
        else:
            return "Bad gateway",502
    

@app.route('/create/task', methods=['POST'])
@cross_origin()
@jwt_required()
def create_task():
    data = request.get_json()
    id = data['id']
    if db.verify_token(get_jwt_identity(), id):
        return "Wrong!", 400
    keys = "(name, list, creation_date"
    token = db.get_token(id)
    name = data["name"]
    name = trim(name)
    if name == "":
        return '400'
    creation_date = time.strftime('%Y-%m-%d %H:%M:%S')
    listt = data["list"]
    value = [name, listt, creation_date]
    if "task" in data:
        task = data["task"]
        keys += ", task"
        value.append(task)
    if "content" in data:
        content = data["content"]
        keys += ", content"
        value.append(content)
    if "deadline" in data:
        deadline = data["deadline"]
        keys += ", deadline"
        value.append(deadline)
    keys += ")"
    value = str(value)
    value = value.replace('[','(')
    value = value.replace(']',')')
    return db.insert("task", keys, value)

@app.route('/delete/task', methods=['POST'])
@cross_origin()
@jwt_required()
def delete_task():
    data = request.get_json()
    id = data["id"]
    if db.verify_token(get_jwt_identity(), id):
        return "Wrong!", 400
    task = data["task"]
    db.delete("task", "id = {}".format(task))
    return "Success", 200


@app.route('/get/task', methods=['POST'])
@cross_origin()
@jwt_required()
def get_task():
    data = request.get_json()
    id = data['id']
    namelist=data['name']
    nametask = data['task']
    if db.verify_token(get_jwt_identity(), data["id"]):
        return "Wrong!", 400
    user = db.fetch('user', cond='id = {}'.format(id))
    listt = db.fetch('`list`', cond="`user` = {} AND `name` = '{}'".format(user[0],namelist))
    if listt:
       task =  db.fetch('`task`', cond='`name` = "{}" AND `content` = "{}" AND `list` = {}'.format(namelist,nametask,listt[0]))
       if task:
           return jsonify(task)
    return "Bad gateway",502
    
    
