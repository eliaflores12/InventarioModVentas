"""Configuración global del sistema: base de datos MySQL, sesiones y variables de entorno."""
import pymysql.cursors
import pymysql

# Parámetros de conexión a la base de datos MySQL (XAMPP)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'Kiosko',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,# Retorna registros como diccionarios en lugar de tuplas
    'autocommit': True,
}

# Llave criptográfica para la firma de cookies de sesión en Flask
SECRET_KEY = 'kiosko-secret-key-2026'

# Credenciales de acceso para el usuario administrador
USUARIO = 'admin'
CLAVE = 'admin123'
# Puerto de ejecución del servidor local
PORT = 8000
# Umbral de unidades para disparar alertas de stock bajo en el inventario
STOCK_MINIMO = 10