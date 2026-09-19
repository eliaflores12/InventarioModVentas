"""Modelo de datos para ventas: transacciones atómicas, control de stock y reportes en MySQL."""
from models.db import get_conexion, query, execute


class Venta:
    """Clase con métodos estáticos para procesar y consultar ventas y sus detalles."""

    @staticmethod
    def registrar(cliente, items):
        """Registra una venta con su detalle y descuenta el stock.
        items es una lista de dicts: {'id': pid, 'cantidad': n}
        Devuelve (venta_id, errores). Si hay errores no se registra nada."""
        conexion = get_conexion()
        cur = conexion.cursor()
        errores = []
        try:
            detalle = []
            for item in items:
                cantidad = item['cantidad']
                if cantidad <= 0:
                    continue
                # Bloqueo a nivel de fila para evitar condiciones de carrera en el stock
                cur.execute('SELECT * FROM productos WHERE id=%s FOR UPDATE', (item['id'],))
                prod = cur.fetchone()
                if not prod:
                    continue
                if prod['stock'] < cantidad:
                    errores.append(f'Stock insuficiente de "{prod["nombre"]}" '
                                   f'(disponible: {prod["stock"]})')
                    continue
                detalle.append((prod, cantidad))

            if not detalle:
                return None, errores or ['Debe agregar al menos un artículo con stock disponible.']
            # Inserta la cabecera de la venta con el total calculado
            total = sum(p['precio'] * c for p, c in detalle)
            cur.execute('INSERT INTO ventas (cliente, total) VALUES (%s,%s)', (cliente, total))
            vid = cur.lastrowid

            # Inserta cada línea de venta y actualiza el inventario restante
            for p, cantidad in detalle:
                subtotal = p['precio'] * cantidad
                cur.execute('INSERT INTO detalle_ventas (venta_id, producto_id, producto_nombre, '
                            'cantidad, precio_unitario, subtotal) VALUES (%s,%s,%s,%s,%s,%s)',
                            (vid, p['id'], p['nombre'], cantidad, p['precio'], subtotal))
                cur.execute('UPDATE productos SET stock = stock - %s WHERE id=%s',
                            (cantidad, p['id']))

            conexion.commit()
            return vid, errores
        except Exception as e:
            # Revierte cualquier cambio en caso de error durante la transacción
            conexion.rollback()
            raise e
        finally:
            cur.close()

    @staticmethod
    def listar(fecha=''):
        """Obtiene el historial de ventas ordenadas cronológicamente, con filtro opcional por fecha."""
        sql = ('SELECT v.*, (SELECT COUNT(*) FROM detalle_ventas d WHERE d.venta_id = v.id) '
               'AS articulos FROM ventas v WHERE 1=1')
        args = []
        if fecha:
            sql += ' AND DATE(v.fecha) = %s'
            args.append(fecha)
        sql += ' ORDER BY v.fecha DESC'
        return query(sql, args)

    @staticmethod
    def obtener(vid):
        """Busca y retorna los datos de cabecera de una venta mediante su ID."""
        return query('SELECT * FROM ventas WHERE id=%s', (vid,), one=True)

    @staticmethod
    def detalle(vid):
        """Retorna la lista de productos y subtotales asociados a una venta."""
        return query('SELECT * FROM detalle_ventas WHERE venta_id=%s', (vid,))

    @staticmethod
    def eliminar(vid):
        """Elimina una venta de la base de datos a partir de su ID."""
        execute('DELETE FROM ventas WHERE id=%s', (vid,))

    @staticmethod
    def ventas_hoy():
        """Calcula la cantidad de transacciones y el monto total recaudado en el día actual."""
        return query('SELECT COUNT(*) AS n, IFNULL(SUM(total),0) AS total '
                     'FROM ventas WHERE DATE(fecha) = CURDATE()', one=True)

    @staticmethod
    def total_acumulado():
        """Calcula el total histórico acumulado de todas las ventas registradas."""
        return query('SELECT IFNULL(SUM(total),0) AS total FROM ventas', one=True)['total']

    @staticmethod
    def ultimas(limite=8):
        """Devuelve las ventas más recientes según el límite especificado."""
        return query('SELECT id, fecha, cliente, total FROM ventas ORDER BY fecha DESC LIMIT %s', (limite,))