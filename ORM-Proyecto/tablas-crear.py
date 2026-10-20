
import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def main():
    conexion = None
    cursor = None

    try:
        # Conectar con la base de datos
        conexion = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conexion.cursor()

        # Crear las tablas de objetos del inventario.
        # No se crea la tabla componentes.
        tablas = [
            """
            CREATE TABLE IF NOT EXISTS categorias (
                id_categoria INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL UNIQUE,
                descripcion TEXT
            ) ENGINE=InnoDB
              DEFAULT CHARSET=utf8mb4
              COLLATE=utf8mb4_unicode_ci
            """,
            """
            CREATE TABLE IF NOT EXISTS marcas (
                id_marca INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL UNIQUE,
                descripcion TEXT
            ) ENGINE=InnoDB
              DEFAULT CHARSET=utf8mb4
              COLLATE=utf8mb4_unicode_ci
            """,
            """
            CREATE TABLE IF NOT EXISTS proveedores (
                id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(150) NOT NULL,
                contacto VARCHAR(100),
                telefono VARCHAR(30),
                email VARCHAR(150),
                direccion VARCHAR(255)
            ) ENGINE=InnoDB
              DEFAULT CHARSET=utf8mb4
              COLLATE=utf8mb4_unicode_ci
            """,
            """
            CREATE TABLE IF NOT EXISTS productos (
                id_producto INT AUTO_INCREMENT PRIMARY KEY,
                codigo VARCHAR(50) NOT NULL UNIQUE,
                nombre VARCHAR(150) NOT NULL,
                descripcion TEXT,
                imagen_url VARCHAR(500),
                modelo VARCHAR(100),
                numero_serie VARCHAR(100),
                id_categoria INT NULL,
                id_marca INT NULL,
                id_proveedor INT NULL,
                precio DECIMAL(12,2) NOT NULL DEFAULT 0.00,
                stock INT NOT NULL DEFAULT 0,
                stock_minimo INT NOT NULL DEFAULT 0,
                ubicacion VARCHAR(100),
                estado VARCHAR(30) NOT NULL DEFAULT 'Disponible',
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (id_categoria)
                    REFERENCES categorias(id_categoria)
                    ON DELETE SET NULL ON UPDATE CASCADE,

                FOREIGN KEY (id_marca)
                    REFERENCES marcas(id_marca)
                    ON DELETE SET NULL ON UPDATE CASCADE,

                FOREIGN KEY (id_proveedor)
                    REFERENCES proveedores(id_proveedor)
                    ON DELETE SET NULL ON UPDATE CASCADE
            ) ENGINE=InnoDB
              DEFAULT CHARSET=utf8mb4
              COLLATE=utf8mb4_unicode_ci
            """
        ]

        for sentencia in tablas:
            cursor.execute(sentencia)

        # Comprobar si componentes existe.
        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.TABLES
            WHERE TABLE_SCHEMA = %s
              AND TABLE_NAME = 'componentes'
        """, (DB_NAME,))

        componentes_existe = cursor.fetchone()[0] > 0

        if componentes_existe:
            # Verificar si historial_estados contiene la FK problemática.
            cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.KEY_COLUMN_USAGE
                WHERE CONSTRAINT_SCHEMA = %s
                  AND TABLE_NAME = 'historial_estados'
                  AND CONSTRAINT_NAME = 'fk_historial_componente'
                  AND REFERENCED_TABLE_NAME = 'componentes'
            """, (DB_NAME,))

            fk_existe = cursor.fetchone()[0] > 0

            if fk_existe:
                cursor.execute("""
                    ALTER TABLE historial_estados
                    DROP FOREIGN KEY fk_historial_componente
                """)
                print("Se quitó la clave foránea que bloqueaba la eliminación.")

            cursor.execute("DROP TABLE componentes")
            print("Tabla componentes eliminada.")
        else:
            print("La tabla componentes ya no existe.")

        conexion.commit()

        print("Tablas de inventario verificadas:")
        print("- categorias")
        print("- marcas")
        print("- proveedores")
        print("- productos")
        print("La tabla historial_estados no se elimina ni se vacía.")

    except mysql.connector.Error as error:
        if conexion is not None and conexion.is_connected():
            conexion.rollback()
        print(f"Error en la base de datos: {error}")

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()


if __name__ == "__main__":
    main()
