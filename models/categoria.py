from models.db import query, execute


class Categoria:

    @staticmethod
    def listar():
        return query('SELECT c.*, COUNT(p.id) AS productos FROM categorias c '
                     'LEFT JOIN productos p ON p.categoria_id = c.id '
                     'GROUP BY c.id ORDER BY c.nombre')

    @staticmethod
    def obtener(cid):
        return query('SELECT * FROM categorias WHERE id=%s', (cid,), one=True)

    @staticmethod
    def guardar(cid, nombre, descripcion):
        if cid:
            execute('UPDATE categorias SET nombre=%s, descripcion=%s WHERE id=%s',
                    (nombre, descripcion, cid))
            return cid
        return execute('INSERT INTO categorias (nombre, descripcion) VALUES (%s,%s)',
                       (nombre, descripcion))

    @staticmethod
    def eliminar(cid):
        execute('DELETE FROM categorias WHERE id=%s', (cid,))