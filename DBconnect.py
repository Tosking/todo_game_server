#!/usr/bin/env python3
import mysql.connector as mysql
from flask_jwt_extended import create_access_token
from datetime import timedelta

class DataBaseConnect:
    def __init__(self):
        DataBaseConnect.conn()

    @classmethod
    def conn(cls):
        con = mysql.connect(
            host = "92.246.214.15",
            user = "ais_sinkevich1858_game_todo",
            passwd = "VVbUPXbt4SFDOPOFANMBBkBd",
            database= "ais_sinkevich1858_game_todo"
        )
        cur = con.cursor(buffered=True)
        return cur, con
    @classmethod
    def fetch(cls,table, cond=None,row='*'):
        cur, con = DataBaseConnect.conn()
        query = "SELECT {} FROM {}".format (row, table, )
        if cond != None:
            query += " WHERE {}".format(cond,)
        print(query)
        cur.execute(query)
        result = cur.fetchall()
        cur.close()
        con.close()
        if result == None or result ==[]:
            return False
        return result[0]
    
    @classmethod
    def insert(cls,table, keys, value):
        cur, con = DataBaseConnect.conn()
        query = "INSERT INTO {}{} VALUES {}".format(table,keys,value)
        print(query)
        cur.execute(query)
        con.commit()
        if cur.rowcount != 0:
            cur.close()
            con.close()
            return True
        cur.close()
        con.close()
        return False
    
    @classmethod
    def delete(cls,table,cond):
        cur,con = DataBaseConnect.conn()
        query = "DELETE FROM `{}` WHERE {}".format(table,cond)
        print(query)
        try:
            cur.execute(query)
            con.commit()
            cur.close()
            con.close()
            return True
        except:
            cur.close()
            con.close()
            return False
    @classmethod
    def update(cls,table, sett, cond):
        cur, con = DataBaseConnect.conn()
        query = "UPDATE `{}` SET {} WHERE {}".format(table, sett, cond)
        print(query)
        try:
            cur.execute(query)
            con.commit()
            cur.close()
            con.close()
            return True
        except:
            cur.close()
            con.close()
            return False
    @classmethod
    def get_token(cls,id ,expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(identity = id,expires_delta=expire_delta)
        return token
    @classmethod
    def verify_token(cls,login, idd):
        query = "SELECT {} FROM {}".format ('*', 'user', )
        query += " WHERE {}".format(idd)
        print("Method verify_token\n Token: ")
        print(query)
        if not query and login != query[3]:
            return True
        return False
