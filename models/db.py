"""Gestor de base de datos: ciclo de vida de conexiones y ejecución de sentencias SQL."""
import pymysql
from flask import g
from config import DB_CONFIG


def get_conexion():
    """Abre o recupera la conexión activa a MySQL almacenada en el contexto de la petición (`flask.g`)."""
    if 'db' not in g:
        g.db = pymysql.connect(**DB_CONFIG)
    return g.db


def cerrar_conexion(exc):
    """Cierra la conexión con MySQL al finalizar el ciclo de vida de la petición HTTP."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def query(sql, args=None, one=False):
    """Ejecuta consultas de lectura (SELECT) y devuelve todas las filas o solo la primera."""
    conexion = get_conexion()
    cur = conexion.cursor()
    cur.execute(sql, args or ())
    filas = cur.fetchall()
    cur.close()
    return (filas[0] if filas else None) if one else filas


def execute(sql, args=None):
    """Ejecuta sentencias de escritura (INSERT, UPDATE, DELETE), confirma la transacción y retorna el ID generado."""
    conexion = get_conexion()
    cur = conexion.cursor()
    cur.execute(sql, args or ())
    ultimo_id = cur.lastrowid
    cur.close()
    conexion.commit()
    return ultimo_id