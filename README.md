# Inventario Mod Ventas — Sistema de Inventarios Licorería

Sistema web MVC para gestión de inventario y ventas de una licorería, construido con **Flask** y **MySQL** (XAMPP).

## Características

- **Autenticación**: login de administrador con sesiones.
- **Dashboard**: total de productos, productos con stock bajo, ventas de hoy, ventas acumuladas, últimos movimientos.
- **Productos**: CRUD completo con búsqueda y filtrado por categoría.
- **Categorías**: CRUD completo.
- **Ventas**: registro de ventas con búsqueda de productos, descuento automático de stock, historial con filtro por fecha y detalle por venta.
- **Búsqueda live de productos** para agilizar el registro de ventas.

## Tecnologías

- Python 3.14+
- Flask 3.1+
- PyMySQL 1.2+
- MySQL (MariaDB en XAMPP)
- Bootstrap 5 (plantillas Jinja2)

## Estructura del proyecto

```
InventarioModVentas/
├── app.py                 # Punto de entrada (Flask app factory)
├── config.py              # Configuración de BD, credenciales y puerto
├── helpers.py             # Utilidades (login_required, formatos)
├── schema.sql             # Esquema y datos iniciales de la BD
├── controllers/           # Blueprints: auth, dashboard, productos, categorias, ventas
├── models/                # Capa de acceso a datos: db, categoria, producto, venta
└── templates/             # Vistas Jinja2 (base, login, dashboard, productos, ventas...)
```

## Base de datos

Ejecuta el esquema para crear la base `licoreria` con datos de ejemplo:

```bash
mysql -u root < schema.sql
```

Tablas:

- `categorias` — catálogo de categorías.
- `productos` — inventario de productos (precio, stock, marca, etc.).
- `ventas` — cabecera de cada venta (cliente, total, fecha).
- `detalle_ventas` — líneas de cada venta con descuento de stock automático.

## Instalación y ejecución

1. Clonar el repositorio:

   ```bash
   git clone <url-del-repositorio>
   cd InventarioModVentas
   ```

2. Crear y activar el entorno virtual (opcional pero recomendado):

   ```bash
   python -m venv venv
   venv\Scripts\activate     # Windows
   ```

3. Instalar dependencias:

   ```bash
   pip install flask pymysql
   ```

4. Configurar la conexión a MySQL en `config.py` (`host`, `user`, `password`, `database`). Por defecto usa XAMPP: usuario `root`, sin contraseña, base `licoreria`.

5. Crear la base de datos:

   ```bash
   mysql -u root < schema.sql
   ```

6. Ejecutar la aplicación:

   ```bash
   python app.py
   ```

7. Abrir en el navegador: <http://127.0.0.1:8000>

## Credenciales de acceso

| Usuario | Clave     |
| ------- | --------- |
| `admin` | `admin123` |

> Cambia las credenciales en `config.py` (`USUARIO`, `CLAVE`) antes de cualquier despliegue real.