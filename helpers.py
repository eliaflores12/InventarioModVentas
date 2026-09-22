"""Módulo de utilidades: decoradores de seguridad y funciones de formato para vistas."""
from functools import wraps
from flask import session, redirect, url_for


def login_required(f):
    """Decorador que restringe el acceso a rutas protegidas si no existe sesión activa."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('logueado'):
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapper


def dinero(valor):
    """Filtro Jinja que convierte un número a formato monetario con separador de miles."""
    valor = valor or 0
    return f'Bs {valor:,.0f}'


def fecha_formato(dt):
    """Filtro Jinja que formatea objetos datetime al formato legible 'DD/MM/AAAA HH:MM AM/PM'."""
    return dt.strftime('%d/%m/%Y %I:%M %p') if dt else ''