"""Controlador de categorías: listar, crear, actualizar y eliminar categorías."""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from helpers import login_required
from models.categoria import Categoria

categorias_bp = Blueprint('categorias', __name__)


@categorias_bp.route('/categorias')
@login_required
def listar():
    """Lista las categorías registradas y carga los datos de edición si se solicita."""
    editar = request.args.get('editar', '')
    editando = Categoria.obtener(editar) if editar else None
    return render_template(
        'categorias.html',
        categorias=Categoria.listar(),
        editando=[editando] if editando else [],
    )


@categorias_bp.route('/categorias/guardar', methods=['POST'])
@login_required
def guardar():
    """Crea una nueva categoría o actualiza una existente según el parámetro 'id'."""
    nombre = request.form.get('nombre', '').strip()
    if not nombre:
        flash('El nombre de la categoria es obligatorio', 'danger')
        return redirect(url_for('categorias.listar'))
    descripcion = request.form.get('descripcion', '').strip()
    cid = request.form.get('id')
    # Guarda o actualiza en la base de datos
    Categoria.guardar(cid, nombre, descripcion)
    flash('Categoria actualizada' if cid else 'Categoria creada', 'success')
    return redirect(url_for('categorias.listar'))


@categorias_bp.route('/categorias/eliminar/<int:cid>')
@login_required
def eliminar(cid):
    """Elimina una categoría por su identificador único (ID)."""
    Categoria.eliminar(cid)
    flash('Categoria eliminada', 'success')
    return redirect(url_for('categorias.listar'))