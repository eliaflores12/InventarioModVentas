from models.db import query, execute


class Producto:

    @staticmethod
    def listar(categoria='', buscar=''):
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
        return query('SELECT * FROM productos WHERE id=%s', (pid,), one=True)

    @staticmethod
    def guardar(pid, datos):
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
        execute('DELETE FROM productos WHERE id=%s', (pid,))

    @staticmethod
    def con_stock():
        return query('SELECT * FROM productos WHERE stock > 0 ORDER BY nombre')

    @staticmethod
    def buscar(termino):
        return query('SELECT id, nombre, precio, stock, marca FROM productos '
                     'WHERE stock > 0 AND (nombre LIKE %s OR marca LIKE %s) ORDER BY nombre LIMIT 10',
                     (f'%{termino}%', f'%{termino}%'))

    @staticmethod
    def conteo():
        return query('SELECT COUNT(*) AS n FROM productos', one=True)['n']

    @staticmethod
    def stock_bajo_conteo(minimo):
        return query('SELECT COUNT(*) AS n FROM productos WHERE stock <= %s', (minimo,), one=True)['n']

    @staticmethod
    def stock_bajo(minimo):
        return query('SELECT * FROM productos WHERE stock <= %s ORDER BY stock ASC LIMIT 10', (minimo,))