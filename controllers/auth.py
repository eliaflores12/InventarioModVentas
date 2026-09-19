from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from config import USUARIO, CLAVE

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    if session.get('logueado'):
        return redirect(url_for('dashboard.index'))
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario', '')
        clave = request.form.get('clave', '')
        if usuario == USUARIO and clave == CLAVE:
            session['logueado'] = True
            session['usuario'] = usuario
            return redirect(url_for('dashboard.index'))
        flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))