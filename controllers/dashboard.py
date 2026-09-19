"""Controlador del dashboard: recopilación y visualización de métricas principales."""
from flask import Blueprint, render_template
from helpers import login_required
from models.producto import Producto
from models.venta import Venta
from config import STOCK_MINIMO

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def index():
    """Consulta métricas generales (inventario, alertas y ventas) y las envía a la vista."""
    # Recopilación de estadísticas e indicadores clave para el panel
    contexto = {
        'productos': Producto.conteo(),
        'stock_bajo': Producto.stock_bajo_conteo(STOCK_MINIMO),
        'ventas_hoy': Venta.ventas_hoy(),
        'ventas_totales': Venta.total_acumulado(),
        'productos_bajos': Producto.stock_bajo(STOCK_MINIMO),
        'ultimas_ventas': Venta.ultimas(),
    }
    return render_template('dashboard.html', **contexto)