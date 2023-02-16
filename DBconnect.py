#!/usr/bin/env python3
import mysql.connector as mysql

def conn():
    con = mysql.connect(
        host = "92.246.214.15",
        user = "ais_sinkevich1858_game_todo",
        passwd = "VVbUPXbt4SFDOPOFANMBBkBd",
        database= "ais_sinkevich1858_game_todo"
    )
    cur = con.cursor(buffered=True)
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
