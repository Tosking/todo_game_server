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

def fetch(table, cond=None,row='*'):
    cur, con = conn()
    query = "SELECT {} FROM {}".format(row,table)
    if cond != None:
        query += " WHERE {}".format(cond)
    print(query)
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    con.close()
    if result == None:
        return False
    else:
        return result[0]

def insert(table, keys, value):
    cur, con = conn()
    query = "INSERT INTO {}{} VALUES {}".format(table, keys, value)
    print(query)
    cur.execute(query)
    con.commit()
    if cur.rowcount != 0:
        cur.close()
        con.close()
        return True
    else:
        cur.close()
        con.close()
        return False


def update(table, sett, cond):
    cur, con = conn()
    query = "UPDATE {} SET {} WHERE {}".format(table, sett, cond)
    try:
        cur.execute(query)
        cur.close()
        con.close()
        return True
    except:
        cur.close()
        con.close()
        return False

def get_token(id ,expire_time=24):
    expire_delta = timedelta(expire_time)
    #id_user = fetch(cur,'user',row='id')
    token = create_access_token(identity = id,expires_delta=expire_delta)
    return token
