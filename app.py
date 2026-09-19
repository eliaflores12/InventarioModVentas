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
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.teardown_appcontext(cerrar_conexion)

    app.jinja_env.filters['dinero'] = dinero
    app.jinja_env.filters['fecha'] = fecha_formato

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(ventas_bp)

    return app


app = create_app()

if __name__ == '__main__':
    print('Sistema de Inventarios Kiosko (MVC)')
    print(f'  Usuario: {USUARIO} | Clave: {CLAVE}')
    print(f'  Abre: http://127.0.0.1:{PORT}')
    app.run(host='0.0.0.0', port=PORT, debug=True, use_reloader=False)