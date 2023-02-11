#!/usr/bin/env python3
import sqlite3

def conn():
    con = sqlite3.connect("DB.sql")
    cur = con.cursor()
    return cur, con

def fetch(cur, table, cond=None):
    query = "SELECT * FROM {}".format(table)
    if cond != None:
        query += " WHERE {}".format(cond)
    return cur.execute(query).fetchall()

def insert(cur, table, keys, value):
    if type(keys) != list:
        keys = list(keys)
    return cur.executemany("INSERT INTO {} VALUES{}".format(table, keys), value)
