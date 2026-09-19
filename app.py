"""Punto de entrada de la aplicación: fábrica de la app Flask y registro de componentes."""
from flask import Flask
from config import SECRET_KEY, PORT, USUARIO, CLAVE

from models.db import cerrar_conexion
from helpers import dinero, fecha_formato

from controllers.auth import auth_bp
from controllers.dashboard import dashboard_bp
from controllers.productos import productos_bp
from controllers.categorias import categorias_bp
from controllers.ventas import ventas_bp


def create_app():
    """Fábrica de la aplicación: configura variables, filtros Jinja, cierre de BD y Blueprints."""
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    # Registra el callback para cerrar conexiones a MySQL al finalizar cada request
    app.teardown_appcontext(cerrar_conexion)

    # Filtros personalizados disponibles en las plantillas Jinja2
    app.jinja_env.filters['dinero'] = dinero
    app.jinja_env.filters['fecha'] = fecha_formato

    # Registro de módulos (Blueprints)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(ventas_bp)

    return app

# Instancia global de la aplicación
app = create_app()

if __name__ == '__main__':
    # Mensaje informativo en consola y arranque del servidor en modo desarrollo
    print('Sistema de Inventarios Kiosko (MVC)')
    print(f'  Usuario: {USUARIO} | Clave: {CLAVE}')
    print(f'  Abre: http://127.0.0.1:{PORT}')
    app.run(host='0.0.0.0', port=PORT, debug=True, use_reloader=False)