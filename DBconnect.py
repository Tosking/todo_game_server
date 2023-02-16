#!/usr/bin/env python3
import mysql.connector as mysql
from flask_jwt_extended import create_access_token
from datetime import timedelta

def conn():
    con = mysql.connect(
        host = "92.246.214.15",
        user = "ais_sinkevich1858_game_todo",
        passwd = "VVbUPXbt4SFDOPOFANMBBkBd",
        database= "ais_sinkevich1858_game_todo"
    )
    cur = con.cursor(buffered=True)
    return cur, con

def fetch(cur,  table, cond=None,row='*'):
    query = "SELECT {} FROM {}".format(row,table)
    if cond != None:
        query += " WHERE {}".format(cond)
    print(query)
    cur.execute(query)
    result = cur.fetchall()
    if result == None:
        return False
    else:
        return result[0]

def insert(cur, con, table, keys, value):
    query = "INSERT INTO {}{} VALUES {}".format(table, keys, value)
    print(query)
    cur.execute(query)
    con.commit()
    if cur.rowcount != 0:
        return True
    else:
        return False


def update(cur, table, sett, cond):
    query = "UPDATE {} SET {} WHERE {}".format(table, sett, cond)
    try:
        cur.execute(query)
        return True
    except:
        return False

def get_token(cur,expire_time=24):
    expire_delta = timedelta(expire_time)
    #id_user = fetch(cur,'user',row='id')
    token = create_access_token(identity = 'id',expires_delta=expire_delta)
    return token
