import pymysql
from flask import g
from config import DB_CONFIG


def get_conexion():
    if 'db' not in g:
        g.db = pymysql.connect(**DB_CONFIG)
    return g.db


def cerrar_conexion(exc):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def query(sql, args=None, one=False):
    conexion = get_conexion()
    cur = conexion.cursor()
    cur.execute(sql, args or ())
    filas = cur.fetchall()
    cur.close()
    return (filas[0] if filas else None) if one else filas


def execute(sql, args=None):
    conexion = get_conexion()
    cur = conexion.cursor()
    cur.execute(sql, args or ())
    ultimo_id = cur.lastrowid
    cur.close()
    conexion.commit()
    return ultimo_id