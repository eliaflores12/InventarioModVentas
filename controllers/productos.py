"""Controlador de productos: gestión del catálogo, filtros y búsqueda AJAX."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from helpers import login_required
from models.producto import Producto
from models.categoria import Categoria

productos_bp = Blueprint('productos', __name__)


@productos_bp.route('/productos')
@login_required
def listar():
    """Muestra el catálogo de productos con filtros por categoría, búsqueda y formulario de edición."""
    categoria = request.args.get('categoria', '')
    buscar = request.args.get('buscar', '')
    editar = request.args.get('editar', '')
    editando = Producto.obtener(editar) if editar else None
    return render_template(
        'productos.html',
        productos=Producto.listar(categoria, buscar),
        categorias=Categoria.listar(),
        categoria=categoria,
        buscar=buscar,
        editando=[editando] if editando else [],
    )


@productos_bp.route('/productos/guardar', methods=['POST'])
@login_required
def guardar():
    """Valida los datos del formulario y registra o actualiza un producto en el inventario."""
    nombre = request.form.get('nombre', '').strip()
    if not nombre:
        flash('El nombre del producto es obligatorio', 'danger')
        return redirect(url_for('productos.listar'))
    # Estructura y casteo de tipos para los campos del producto
    datos = {
        'nombre': nombre,
        'categoria_id': request.form.get('categoria_id') or None,
        'precio': float(request.form.get('precio') or 0),
        'stock': int(request.form.get('stock') or 0),
        'marca': request.form.get('marca', '').strip(),
        'descripcion': request.form.get('descripcion', '').strip(),
    }
    pid = request.form.get('id')
    Producto.guardar(pid, datos)
    flash('Producto actualizado correctamente' if pid else 'Producto creado correctamente', 'success')
    return redirect(url_for('productos.listar'))


@productos_bp.route('/productos/eliminar/<int:pid>')
@login_required
def eliminar(pid):
    """Elimina un producto del catálogo por su ID."""
    Producto.eliminar(pid)
    flash('Producto eliminado', 'success')
    return redirect(url_for('productos.listar'))


@productos_bp.route('/buscar_producto')
@login_required
def buscar():
    """Endpoint tipo API que devuelve coincidencias de productos en formato JSON para autocompletado."""
    termino = request.args.get('q', '')
    if not termino:
        return jsonify([])
    return jsonify(Producto.buscar(termino))