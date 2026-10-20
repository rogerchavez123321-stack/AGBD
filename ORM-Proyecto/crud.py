
import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")


def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def listar_productos():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT id_producto, codigo, nombre, descripcion,
                   modelo, numero_serie, precio, stock,
                   stock_minimo, ubicacion, estado
            FROM productos
            ORDER BY id_producto
        """)

        productos = cursor.fetchall()

        if not productos:
            print("No hay productos registrados.")
            return

        for p in productos:
            print(
                f"\nID: {p['id_producto']} | "
                f"Código: {p['codigo']} | "
                f"Nombre: {p['nombre']}"
            )
            print(
                f"Modelo: {p['modelo']} | "
                f"Serie: {p['numero_serie']}"
            )
            print(
                f"Precio: {p['precio']} | "
                f"Stock: {p['stock']} | "
                f"Mínimo: {p['stock_minimo']}"
            )
            print(
                f"Ubicación: {p['ubicacion']} | "
                f"Estado: {p['estado']}"
            )

    finally:
        cursor.close()
        conexion.close()


def crear_producto():
    codigo = input("Código único: ").strip()
    nombre = input("Nombre: ").strip()
    descripcion = input("Descripción: ").strip() or None
    imagen_url = input("URL de imagen (opcional): ").strip() or None
    modelo = input("Modelo: ").strip() or None
    numero_serie = input("Número de serie: ").strip() or None
    ubicacion = input("Ubicación: ").strip() or None
    estado = input("Estado [Disponible]: ").strip() or "Disponible"

    if not codigo or not nombre:
        print("El código y el nombre son obligatorios.")
        return

    try:
        precio = float(input("Precio: "))
        stock = int(input("Stock actual: "))
        stock_minimo = int(input("Stock mínimo: "))

        if precio < 0 or stock < 0 or stock_minimo < 0:
            print("El precio y el stock no pueden ser negativos.")
            return

    except ValueError:
        print("Ingresá un precio y cantidades válidas.")
        return

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            INSERT INTO productos (
                codigo, nombre, descripcion, imagen_url,
                modelo, numero_serie, precio, stock,
                stock_minimo, ubicacion, estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            codigo, nombre, descripcion, imagen_url,
            modelo, numero_serie, precio, stock,
            stock_minimo, ubicacion, estado
        ))

        conexion.commit()
        print(f"Producto creado con ID {cursor.lastrowid}.")

    except mysql.connector.Error as error:
        conexion.rollback()
        print(f"No se pudo crear el producto: {error}")

    finally:
        cursor.close()
        conexion.close()


def modificar_producto():
    try:
        id_producto = int(input("ID del producto a modificar: "))
    except ValueError:
        print("El ID debe ser un número entero.")
        return

    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM productos WHERE id_producto = %s",
            (id_producto,)
        )
        producto = cursor.fetchone()

        if not producto:
            print("No existe un producto con ese ID.")
            return

        print("Dejá vacío un campo para conservar su valor.")

        campos = [
            ("codigo", "Código"),
            ("nombre", "Nombre"),
            ("descripcion", "Descripción"),
            ("imagen_url", "URL de imagen"),
            ("modelo", "Modelo"),
            ("numero_serie", "Número de serie"),
            ("ubicacion", "Ubicación"),
            ("estado", "Estado")
        ]

        cambios = {}

        for campo, etiqueta in campos:
            actual = producto[campo]
            nuevo = input(f"{etiqueta} [{actual or ''}]: ").strip()

            if nuevo:
                cambios[campo] = nuevo

        for campo, etiqueta in [
            ("precio", "Precio"),
            ("stock", "Stock"),
            ("stock_minimo", "Stock mínimo")
        ]:
            actual = producto[campo]
            nuevo = input(f"{etiqueta} [{actual}]: ").strip()

            if nuevo:
                try:
                    valor = float(nuevo) if campo == "precio" else int(nuevo)

                    if valor < 0:
                        print(f"{etiqueta} no puede ser negativo.")
                        return

                    cambios[campo] = valor

                except ValueError:
                    print(f"Valor inválido para {etiqueta}.")
                    return

        if not cambios:
            print("No se realizaron cambios.")
            return

        if "codigo" in cambios and not cambios["codigo"]:
            print("El código no puede estar vacío.")
            return

        if "nombre" in cambios and not cambios["nombre"]:
            print("El nombre no puede estar vacío.")
            return

        cursor.execute("SELECT id_categoria FROM categorias LIMIT 0")
        # La consulta anterior solo verifica la tabla; no modifica datos.

        cursor.execute(
            "SELECT id_producto FROM productos WHERE codigo = %s "
            "AND id_producto <> %s",
            (cambios.get("codigo", producto["codigo"]), id_producto)
        )

        if cursor.fetchone():
            print("Ese código ya pertenece a otro producto.")
            return

        asignaciones = ", ".join(
            f"`{campo}` = %s" for campo in cambios
        )
        valores = list(cambios.values()) + [id_producto]

        cursor.execute(
            f"UPDATE productos SET {asignaciones} WHERE id_producto = %s",
            valores
        )

        conexion.commit()
        print("Producto actualizado correctamente.")

    except mysql.connector.Error as error:
        conexion.rollback()
        print(f"No se pudo modificar el producto: {error}")

    finally:
        cursor.close()
        conexion.close()


def eliminar_producto():
    try:
        id_producto = int(input("ID del producto a eliminar: "))
    except ValueError:
        print("El ID debe ser un número entero.")
        return

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "SELECT nombre FROM productos WHERE id_producto = %s",
            (id_producto,)
        )
        producto = cursor.fetchone()

        if not producto:
            print("No existe un producto con ese ID.")
            return

        confirmacion = input(
            f"¿Eliminar '{producto[0]}'? Escribí SI para confirmar: "
        )

        if confirmacion != "SI":
            print("Operación cancelada.")
            return

        cursor.execute(
            "DELETE FROM productos WHERE id_producto = %s",
            (id_producto,)
        )

        conexion.commit()
        print("Producto eliminado correctamente.")

    except mysql.connector.Error as error:
        conexion.rollback()
        print(f"No se pudo eliminar el producto: {error}")

    finally:
        cursor.close()
        conexion.close()


def main():
    while True:
        print("""
======== STOCK-CONTROLER ========
1. Listar productos
2. Crear producto
3. Modificar producto
4. Eliminar producto
5. Salir
""")

        opcion = input("Elegí una opción: ").strip()

        try:
            if opcion == "1":
                listar_productos()
            elif opcion == "2":
                crear_producto()
            elif opcion == "3":
                modificar_producto()
            elif opcion == "4":
                eliminar_producto()
            elif opcion == "5":
                print("Programa finalizado.")
                break
            else:
                print("Opción inválida.")

        except mysql.connector.Error as error:
            print(f"Error de conexión o base de datos: {error}")


if __name__ == "__main__":
    main()
