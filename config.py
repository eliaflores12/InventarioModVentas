import pymysql.cursors
import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'licoreria',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
    'autocommit': True,
}

SECRET_KEY = 'licoreria-secret-key-2026'
USUARIO = 'admin'
CLAVE = 'admin123'
PORT = 8000
STOCK_MINIMO = 10