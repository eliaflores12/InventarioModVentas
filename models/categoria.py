"""Modelo de datos para categorías: operaciones SQL sobre la tabla 'categorias'."""
from models.db import query, execute


class Categoria:
    """Clase con métodos estáticos para la persistencia y consulta de categorías."""
    @staticmethod
    def listar():
        """Obtiene todas las categorías ordenadas por nombre, incluyendo el conteo de productos asociados."""
        return query('SELECT c.*, COUNT(p.id) AS productos FROM categorias c '
                     'LEFT JOIN productos p ON p.categoria_id = c.id '
                     'GROUP BY c.id ORDER BY c.nombre')

    @staticmethod
    def obtener(cid):
        """Busca y retorna una sola categoría según su ID."""
        return query('SELECT * FROM categorias WHERE id=%s', (cid,), one=True)

    @staticmethod
    def guardar(cid, nombre, descripcion):
        """Inserta una nueva categoría o actualiza una existente si se proporciona un ID."""
        if cid:
            execute('UPDATE categorias SET nombre=%s, descripcion=%s WHERE id=%s',
                    (nombre, descripcion, cid))
            return cid
        return execute('INSERT INTO categorias (nombre, descripcion) VALUES (%s,%s)',
                       (nombre, descripcion))

    @staticmethod
    def eliminar(cid):
        """Elimina una categoría de la base de datos a partir de su ID."""  
        execute('DELETE FROM categorias WHERE id=%s', (cid,))