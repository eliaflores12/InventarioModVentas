from flask import Blueprint, render_template, request, redirect, url_for, flash
from helpers import login_required, dinero
from models.venta import Venta
from models.producto import Producto

ventas_bp = Blueprint('ventas', __name__)


@ventas_bp.route('/ventas/nueva')
@login_required
def nueva():
    return render_template('ventas_new.html', productos=Producto.con_stock())


@ventas_bp.route('/ventas/registrar', methods=['POST'])
@login_required
def registrar():
    cliente = request.form.get('cliente', 'Consumidor final') or 'Consumidor final'
    productos_id = request.form.getlist('producto_id[]')
    cantidades = request.form.getlist('cantidad[]')

    items = []
    for pid, cant in zip(productos_id, cantidades):
        if not pid:
            continue
        try:
            cantidad = int(cant)
        except (TypeError, ValueError):
            cantidad = 0
        items.append({'id': pid, 'cantidad': cantidad})

    try:
        vid, errores = Venta.registrar(cliente, items)
    except Exception as e:
        flash(f'Error al registrar la venta: {e}', 'danger')
        return redirect(url_for('ventas.nueva'))

    for err in errores:
        flash(err, 'danger')

    if vid:
        flash(f'Venta #{vid} registrada por {dinero(Venta.obtener(vid)["total"])}', 'success')
        return redirect(url_for('ventas.detalle', vid=vid))

    return redirect(url_for('ventas.nueva'))


@ventas_bp.route('/ventas')
@login_required
def listar():
    fecha = request.args.get('fecha', '')
    filas = Venta.listar(fecha)
    return render_template('ventas.html', ventas=filas, fecha=fecha,
                           total_filtrado=sum(v['total'] for v in filas))


@ventas_bp.route('/ventas/<int:vid>')
@login_required
def detalle(vid):
    venta = Venta.obtener(vid)
    if not venta:
        flash('Venta no encontrada', 'warning')
        return redirect(url_for('ventas.listar'))
    return render_template('venta_detalle.html', venta=venta, detalle=Venta.detalle(vid))


@ventas_bp.route('/ventas/eliminar/<int:vid>')
@login_required
def eliminar(vid):
    Venta.eliminar(vid)
    flash('Venta eliminada', 'success')
    return redirect(url_for('ventas.listar'))