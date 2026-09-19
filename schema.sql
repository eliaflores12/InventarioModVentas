CREATE DATABASE IF NOT EXISTS licoreria CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE licoreria;

DROP TABLE IF EXISTS detalle_ventas;
DROP TABLE IF EXISTS ventas;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS categorias;

CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion VARCHAR(255)
) ENGINE=InnoDB;

CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    categoria_id INT,
    precio DECIMAL(10,2) NOT NULL DEFAULT 0,
    stock INT NOT NULL DEFAULT 0,
    marca VARCHAR(100),
    descripcion VARCHAR(255),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cliente VARCHAR(150),
    total DECIMAL(10,2) NOT NULL DEFAULT 0
) ENGINE=InnoDB;

CREATE TABLE detalle_ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venta_id INT NOT NULL,
    producto_id INT,
    producto_nombre VARCHAR(150),
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES ventas(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE SET NULL
) ENGINE=InnoDB;

INSERT INTO categorias (nombre, descripcion) VALUES
('Cervezas', 'Cervezas nacionales e importadas'),
('Machucados', 'Hoja de coca con saborizantes '),
('Whisky', 'Whiskies nacionales y de importacion'),
('Cigarrillos', 'Nacionales e importados'),
('Sin alcohol', 'Refrescos, jugos y energizantes');

INSERT INTO productos (nombre, categoria_id, precio, stock, marca, descripcion) VALUES
('Paceña ', 1, 10, 120, 'Paceña', 'Cerveza ligera en lata 269ml'),
('Huari', 1, 15, 150, 'Huari', 'Cerveza clasica en lata 269,440ml'),
('WiskY Blak Stone', 3, 70, 40, 'Black Stone', 'Wiski Importado en botella 1000ml'),
('Machucado Maracuya', 2, 18, 6, 'Mi Negrita', 'tiene un peso de 55g'),
('Devy Antiguo', 4, 12, 70, 'CITSA', 'Version Tradicional de 20ud'),
('Powerade Mora AZul', 5, 12, 30, 'Cocacola', 'Bebida isotónica 990ml');