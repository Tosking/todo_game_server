#!/usr/bin/env python3
import mysql.connector as mysql

def conn():
    con = mysql.connect(
        host = "92.246.214.15",
        user = "ais_sinkevich1858_game_todo",
        passwd = "VVbUPXbt4SFDOPOFANMBBkBd",
        database= "ais_sinkevich1858_game_todo"
    )
    cur = con.cursor()
    return cur, con

def fetch(cur, table, cond=None):
    query = "SELECT * FROM {}".format(table)
    if cond != None:
        query += " WHERE {}".format(cond)
    print(query)
    result = cur.execute(query)
    if result == None:
        return None
    else:
        return cur.execute(query).fetchall()

def insert(cur, table, keys, value):
    if type(keys) != list:
        keys = list(keys)
    return cur.executemany("INSERT INTO {} VALUES{}".format(table, keys), value)
