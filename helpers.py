from functools import wraps
from flask import session, redirect, url_for


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('logueado'):
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapper


def dinero(valor):
    valor = valor or 0
    return f'${valor:,.0f}'


def fecha_formato(dt):
    return dt.strftime('%d/%m/%Y %I:%M %p') if dt else ''