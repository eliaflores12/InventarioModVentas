"""Modelo de datos para productos: consultas, filtros y operaciones de inventario en MySQL."""
from models.db import query, execute


class Producto:
    """Clase con métodos estáticos para la gestión y persistencia del catálogo de productos."""

    @staticmethod
    def listar(categoria='', buscar=''):
        """Obtiene la lista de productos uniendo su categoría, con filtros opcionales de búsqueda y categoría."""
        sql = ('SELECT p.*, c.nombre AS categoria FROM productos p '
               'LEFT JOIN categorias c ON c.id = p.categoria_id WHERE 1=1')
        args = []
        if buscar:
            sql += ' AND (p.nombre LIKE %s OR p.marca LIKE %s)'
            args += [f'%{buscar}%', f'%{buscar}%']
        if categoria:
            sql += ' AND p.categoria_id = %s'
            args.append(categoria)
        sql += ' ORDER BY p.nombre'
        return query(sql, args)

    @staticmethod
    def obtener(pid):
        """Busca y retorna los datos de un producto específico mediante su ID."""
        return query('SELECT * FROM productos WHERE id=%s', (pid,), one=True)

    @staticmethod
    def guardar(pid, datos):
        """Inserta un nuevo producto o actualiza sus atributos si se proporciona un ID."""
        if pid:
            execute('UPDATE productos SET nombre=%s, categoria_id=%s, precio=%s, stock=%s, '
                    'marca=%s, descripcion=%s WHERE id=%s',
                    (datos['nombre'], datos['categoria_id'], datos['precio'],
                     datos['stock'], datos['marca'], datos['descripcion'], pid))
            return pid
        return execute('INSERT INTO productos (nombre, categoria_id, precio, stock, marca, descripcion) '
                       'VALUES (%s,%s,%s,%s,%s,%s)',
                       (datos['nombre'], datos['categoria_id'], datos['precio'],
                        datos['stock'], datos['marca'], datos['descripcion']))

    @staticmethod
    def eliminar(pid):
        """Elimina un producto de la base de datos por su ID."""
        execute('DELETE FROM productos WHERE id=%s', (pid,))

    @staticmethod
    def con_stock():
        """Devuelve únicamente los productos con existencias disponibles (stock mayor a cero)."""
        return query('SELECT * FROM productos WHERE stock > 0 ORDER BY nombre')

    @staticmethod
    def buscar(termino):
        """Busca hasta 10 productos con existencias disponibles por coincidencia en nombre o marca."""
        return query('SELECT id, nombre, precio, stock, marca FROM productos '
                     'WHERE stock > 0 AND (nombre LIKE %s OR marca LIKE %s) ORDER BY nombre LIMIT 10',
                     (f'%{termino}%', f'%{termino}%'))

    @staticmethod
    def conteo():
        """Retorna el total de productos registrados en el sistema."""
        return query('SELECT COUNT(*) AS n FROM productos', one=True)['n']

    @staticmethod
    def stock_bajo_conteo(minimo):
        """Calcula el número de productos cuyo stock es igual o inferior al umbral mínimo."""
        return query('SELECT COUNT(*) AS n FROM productos WHERE stock <= %s', (minimo,), one=True)['n']

    @staticmethod
    def stock_bajo(minimo):
        """Obtiene hasta 10 productos en situación de alerta por bajo stock ordenados de forma ascendente."""
        return query('SELECT * FROM productos WHERE stock <= %s ORDER BY stock ASC LIMIT 10', (minimo,))