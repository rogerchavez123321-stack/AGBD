#-------------#
#Codigo "1"
#-------------#
import sqlite3

conn = sqlite3.connect("mi_app.db")
conn.row_factory = sqlite3.Row  # <- esto reemplaza la conversión manual a diccionario
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nombre TEXT,
        email TEXT,
        activo INTEGER
    )
""")

# INSERT OR IGNORE evita el error si el id ya existe (permite re-ejecutar el script)
cursor.execute(
    "INSERT OR IGNORE INTO usuarios VALUES (?, ?, ?, ?)",
    (1, 'Ana García', 'ana@mail.com', 1)
)
conn.commit()

cursor.execute("""
    SELECT id, nombre, email FROM usuarios WHERE activo = 1
""")
rows = cursor.fetchall()

# Ya no hace falta armar el diccionario a mano:
# row_factory = sqlite3.Row permite acceder por nombre de columna
usuarios = [dict(row) for row in rows]

conn.close()

print(usuarios)

#-------------------#
#Codigo "2"
#-------------------#
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import DeclarativeBase, Session

# 1. Definimos la clase (una sola vez)
class Base(DeclarativeBase):
    pass

class Usuario(Base):
    __tablename__ = "usuarios"

    id      = Column(Integer, primary_key=True)
    nombre  = Column(String)
    email   = Column(String)
    activo  = Column(Boolean)

# 2. Consultamos como si fueran objetos Python
engine = create_engine("sqlite:///mi_app.db")

with Session(engine) as session:
    usuarios = session.query(Usuario) \
                      .filter(Usuario.activo == True) \
                      .all()

    for u in usuarios:
        print(u.nombre, u.email)  # ← atributos reales, no índices
#-------------------#
#Codigo "3"
#-------------------#
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    pass

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    precio = Column(Float)
    stock = Column(Integer)
    categoria = Column(String)


engine = create_engine("sqlite:///:memory:", echo=True)


Base.metadata.create_all(engine)


with Session(engine) as session:
    p1 = Producto(nombre="Cuaderno", precio=350.0, stock=20, categoria="Librería")
    p2 = Producto(nombre="Lapicera", precio=120.0, stock=50, categoria="Librería")
    p3 = Producto(nombre="Mochila", precio=1500.0, stock=5, categoria="Librería")
    p4 = Producto(nombre="Goma de borrar", precio=80.0, stock=100, categoria="Librería")
    p5 = Producto(nombre="Regra", precio=600.0, stock=15, categoria="Librería")

    session.add_all([p1, p2, p3, p4, p5])
    session.commit()

with Session(engine) as session:
    productos_baratos = (
        session.query(Producto)
        .filter(Producto.precio < 500)
        .all()
    )

    print("\n--- PRODUCTOS CON PRECIO MENOR A $500 ---")
    for prod in productos_baratos:
        print(f"Producto: {prod.nombre} | Precio: ${prod.precio} | Stock: {prod.stock} | Categoría: {prod.categoria}")




#------------------------------------ORM-Practicas-----------------------------#

from sqlalchemy import Boolean, Column, Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Session



class Base(DeclarativeBase):
    pass



class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    categoria = Column(String)
    precio = Column(Float)
    stock = Column(Integer)
    activo = Column(Boolean, default=True)



engine = create_engine("sqlite:///:memory:", echo=True)


Base.metadata.create_all(engine)


with Session(engine) as session:
    p1 = Producto(nombre="Cuaderno", precio=350.0, stock=20, categoria="Librería")
    p2 = Producto(nombre="Lapicera", precio=120.0, stock=50, categoria="Librería")
    p3 = Producto(nombre="Mochila", precio=1500.0, stock=5, categoria="Librería")
    p4 = Producto(nombre="Goma de borrar", precio=80.0, stock=100, categoria="Librería")
    p5 = Producto(nombre="Regla", precio=600.0, stock=15, categoria="Librería")

    session.add_all([p1, p2, p3, p4, p5])
    session.commit()


with Session(engine) as session:
    productos_baratos = (
        session.query(Producto).filter(Producto.precio < 500).all()
    )

    print("\n--- PRODUCTOS CON PRECIO MENOR A $500 ---")
    for prod in productos_baratos:
        print(f"ID: {prod.id}  Producto: {prod.nombre}  Precio: ${prod.precio}  "f"Stock: {prod.stock}  Categoría: {prod.categoria}  Activo: {prod.activo}")

#-------------EJERCICIO-2-------------------#

from sqlalchemy import Boolean, Column, Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    pass


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    categoria = Column(String)
    precio = Column(Float)
    stock = Column(Integer)
    activo = Column(Boolean, default=True)


engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)


with Session(engine) as session:
    productos = [
        Producto(nombre="Teclado mecanico", categoria="perifericos", precio=8500.0, stock=15),
        Producto(nombre="Mouse inalambrico", categoria="perifericos", precio=4200.0, stock=30),
        Producto(nombre="Monitor 24 pulgadas", categoria="monitores", precio=62000.0, stock=8),
        Producto(nombre="Auriculares bluetooth", categoria="audio", precio=12300.0, stock=20),
        Producto(nombre="Webcam Full HD", categoria="perifericos", precio=9800.0, stock=12),
        Producto(nombre="SSD 1TB", categoria="almacenamiento", precio=18500.0, stock=25),
        Producto(nombre="RAM 16GB", categoria="componentes", precio=15600.0, stock=18),
        Producto(nombre="Mousepad XL", categoria="perifericos", precio=2100.0, stock=40),
        Producto(nombre="Hub USB-C", categoria="accesorios", precio=5400.0, stock=6, activo=False),
        Producto(nombre="Cable HDMI", categoria="accesorios", precio=1800.0, stock=50),
    ]

    session.add_all(productos)
    session.commit()

# Verificación de la cantidad de productos
with Session(engine) as session:
    total_productos = session.query(Producto).count()
    print(f"Total de productos en la base de datos: {total_productos}")      




#---------EJERCICIO-3-----------#
from sqlalchemy import Boolean, Column, Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Session



class Base(DeclarativeBase):
    pass


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    categoria = Column(String)
    precio = Column(Float)
    stock = Column(Integer)
    activo = Column(Boolean, default=True)



engine = create_engine("sqlite:///:memory:", echo=False)
Base.metadata.create_all(engine)



with Session(engine) as session:
    productos = [
        Producto(nombre="Teclado mecanico", categoria="perifericos", precio=8500.0, stock=15),
        Producto(nombre="Mouse inalambrico", categoria="perifericos", precio=4200.0, stock=30),
        Producto(nombre="Monitor 24 pulgadas", categoria="monitores", precio=62000.0, stock=8),
        Producto(nombre="Auriculares bluetooth", categoria="audio", precio=12300.0, stock=20),
        Producto(nombre="Webcam Full HD", categoria="perifericos", precio=9800.0, stock=12),
        Producto(nombre="SSD 1TB", categoria="almacenamiento", precio=18500.0, stock=25),
        Producto(nombre="RAM 16GB", categoria="componentes", precio=15600.0, stock=18),
        Producto(nombre="Mousepad XL", categoria="perifericos", precio=2100.0, stock=40),
        Producto(nombre="Hub USB-C", categoria="accesorios", precio=5400.0, stock=6, activo=False),
        Producto(nombre="Cable HDMI", categoria="accesorios", precio=1800.0, stock=50),
    ]

    session.add_all(productos)
    session.commit()


with Session(engine) as session:
    total = session.query(Producto).count()
    print(f"Total de productos registrados: {total}")



with Session(engine) as session:
    perifericos = (
        session.query(Producto)
        .filter(Producto.categoria == "perifericos")
        .all()
    )

    print("\n--- PRODUCTOS DE LA CATEGORÍA PERIFERICOS ---")
    for prod in perifericos:
        print(f"Nombre: {prod.nombre} | Precio: ${prod.precio}")

#-------------EJERCICIO-4------------------#
from sqlalchemy import Boolean, Column, Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    pass


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    categoria = Column(String)
    precio = Column(Float)
    stock = Column(Integer)
    activo = Column(Boolean, default=True)



engine = create_engine("sqlite:///:memory:", echo=False)
Base.metadata.create_all(engine)



with Session(engine) as session:
    productos = [
        Producto(nombre="Teclado mecanico", categoria="perifericos", precio=8500.0, stock=15),
        Producto(nombre="Mouse inalambrico", categoria="perifericos", precio=4200.0, stock=30),
        Producto(nombre="Monitor 24 pulgadas", categoria="monitores", precio=62000.0, stock=8),
        Producto(nombre="Auriculares bluetooth", categoria="audio", precio=12300.0, stock=20),
        Producto(nombre="Webcam Full HD", categoria="perifericos", precio=9800.0, stock=12),
        Producto(nombre="SSD 1TB", categoria="almacenamiento", precio=18500.0, stock=25),
        Producto(nombre="RAM 16GB", categoria="componentes", precio=15600.0, stock=18),
        Producto(nombre="Mousepad XL", categoria="perifericos", precio=2100.0, stock=40),
        Producto(nombre="Hub USB-C", categoria="accesorios", precio=5400.0, stock=6, activo=False),
        Producto(nombre="Cable HDMI", categoria="accesorios", precio=1800.0, stock=50),
    ]

    session.add_all(productos)
    session.commit()



with Session(engine) as session:
    perifericos = (
        session.query(Producto)
        .filter(Producto.categoria == "perifericos")
        .all()
    )

    print("\n--- PRODUCTOS DE LA CATEGORÍA PERIFERICOS ---")
    for prod in perifericos:
        print(f"Nombre: {prod.nombre} | Precio: ${prod.precio}")



with Session(engine) as session:
    productos_caros = (
        session.query(Producto)
        .filter(Producto.precio > 10000)
        .order_by(Producto.precio.desc())
        .all()
    )

    print("\n--- PRODUCTOS MAYORES A $10000 ---")
    for prod in productos_caros:
        print(f"Nombre: {prod.nombre} | Precio: ${prod.precio}")

#----------------EJERCICIO-5-------------------#
#El Hub USB-C no aparece porque, aunque cumple con tener un stock menor a 12 (tiene stock 6),
#tiene el campo activo=False. La condición exige que se cumplan ambas reglas al mismo tiempo 
#(que el stock sea menor o igual a 12 Y que el producto esté activo).

from sqlalchemy import Boolean, Column, Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Session



class Base(DeclarativeBase):
    pass



class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    categoria = Column(String)
    precio = Column(Float)
    stock = Column(Integer)
    activo = Column(Boolean, default=True)



engine = create_engine("sqlite:///:memory:", echo=False)
Base.metadata.create_all(engine)



with Session(engine) as session:
    productos = [
        Producto(nombre="Teclado mecanico", categoria="perifericos", precio=8500.0, stock=15),
        Producto(nombre="Mouse inalambrico", categoria="perifericos", precio=4200.0, stock=30),
        Producto(nombre="Monitor 24 pulgadas", categoria="monitores", precio=62000.0, stock=8),
        Producto(nombre="Auriculares bluetooth", categoria="audio", precio=12300.0, stock=20),
        Producto(nombre="Webcam Full HD", categoria="perifericos", precio=9800.0, stock=12),
        Producto(nombre="SSD 1TB", categoria="almacenamiento", precio=18500.0, stock=25),
        Producto(nombre="RAM 16GB", categoria="componentes", precio=15600.0, stock=18),
        Producto(nombre="Mousepad XL", categoria="perifericos", precio=2100.0, stock=40),
        Producto(nombre="Hub USB-C", categoria="accesorios", precio=5400.0, stock=6, activo=False),
        Producto(nombre="Cable HDMI", categoria="accesorios", precio=1800.0, stock=50),
    ]

    session.add_all(productos)
    session.commit()



with Session(engine) as session:
    perifericos = (
        session.query(Producto)
        .filter(Producto.categoria == "perifericos")
        .all()
    )

    print("\n--- PRODUCTOS DE LA CATEGORÍA PERIFERICOS ---")
    for prod in perifericos:
        print(f"Nombre: {prod.nombre}  Precio: ${prod.precio}")



with Session(engine) as session:
    productos_caros = (
        session.query(Producto)
        .filter(Producto.precio > 10000)
        .order_by(Producto.precio.desc())
        .all()
    )

    print("\n--- PRODUCTOS MAYORES A $10000 ---")
    for prod in productos_caros:
        print(f"Nombre: {prod.nombre}  Precio: ${prod.precio}")



with Session(engine) as session:
    bajo_stock_activos = (
        session.query(Producto)
        .filter(Producto.stock <= 12, Producto.activo == True)
        .all()
    )

    print("\n--- PRODUCTOS CON STOCK <= 12 Y ACTIVOS ---")
    for prod in bajo_stock_activos:
        print(
            f"Nombre: {prod.nombre}  Stock: {prod.stock}  Activo: {prod.activo}"
        )

#---------------------EJERCICIO-6------------------#
from sqlalchemy import Boolean, Column, Float, Integer, String, create_engine, and_
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    pass


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    categoria = Column(String)
    precio = Column(Float)
    stock = Column(Integer)
    activo = Column(Boolean, default=True)



engine = create_engine("sqlite:///:memory:", echo=False)
Base.metadata.create_all(engine)


with Session(engine) as session:
    productos = [
        Producto(nombre="Teclado mecanico", categoria="perifericos", precio=8500.0, stock=15),
        Producto(nombre="Mouse inalambrico", categoria="perifericos", precio=4200.0, stock=30),
        Producto(nombre="Monitor 24 pulgadas", categoria="monitores", precio=62000.0, stock=8),
        Producto(nombre="Auriculares bluetooth", categoria="audio", precio=12300.0, stock=20),
        Producto(nombre="Webcam Full HD", categoria="perifericos", precio=9800.0, stock=12),
        Producto(nombre="SSD 1TB", categoria="almacenamiento", precio=18500.0, stock=25),
        Producto(nombre="RAM 16GB", categoria="componentes", precio=15600.0, stock=18),
        Producto(nombre="Mousepad XL", categoria="perifericos", precio=2100.0, stock=40),
        Producto(nombre="Hub USB-C", categoria="accesorios", precio=5400.0, stock=6, activo=False),
        Producto(nombre="Cable HDMI", categoria="accesorios", precio=1800.0, stock=50),
    ]

    session.add_all(productos)
    session.commit()



with Session(engine) as session:
    perifericos = (
        session.query(Producto)
        .filter(Producto.categoria == "perifericos")
        .all()
    )

    print("\n--- PRODUCTOS DE LA CATEGORÍA PERIFERICOS ---")
    for prod in perifericos:
        print(f"Nombre: {prod.nombre} | Precio: ${prod.precio}")



with Session(engine) as session:
    productos_caros = (
        session.query(Producto)
        .filter(Producto.precio > 10000)
        .order_by(Producto.precio.desc())
        .all()
    )

    print("\n--- PRODUCTOS MAYORES A $10000 ---")
    for prod in productos_caros:
        print(f"Nombre: {prod.nombre} | Precio: ${prod.precio}")



with Session(engine) as session:
    bajo_stock_activos = (
        session.query(Producto)
        .filter(Producto.stock <= 12, Producto.activo == True)
        .all()
    )

    print("\n--- PRODUCTOS CON STOCK <= 12 Y ACTIVOS ---")
    for prod in bajo_stock_activos:
        print(
            f"Nombre: {prod.nombre} | Stock: {prod.stock} | Activo: {prod.activo}"
        )



with Session(engine) as session:
    rango_precio = (
        session.query(Producto)
        .filter(and_(Producto.precio >= 5000, Producto.precio <= 20000))
        .all()
    )

    print("\n--- PRODUCTOS CON PRECIO ENTRE $5000 Y $20000 ---")
    for prod in rango_precio:
        print(f"Nombre: {prod.nombre}  Precio: ${prod.precio}")

#-------------------EJERCICIO-7---------------------#
from sqlalchemy import Boolean, Column, Float, Integer, String, create_engine, and_
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    pass


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    categoria = Column(String)
    precio = Column(Float)
    stock = Column(Integer)
    activo = Column(Boolean, default=True)


engine = create_engine("sqlite:///:memory:", echo=False)
Base.metadata.create_all(engine)


with Session(engine) as session:
    productos = [
        Producto(nombre="Teclado mecanico", categoria="perifericos", precio=8500.0, stock=15),
        Producto(nombre="Mouse inalambrico", categoria="perifericos", precio=4200.0, stock=30),
        Producto(nombre="Monitor 24 pulgadas", categoria="monitores", precio=62000.0, stock=8),
        Producto(nombre="Auriculares bluetooth", categoria="audio", precio=12300.0, stock=20),
        Producto(nombre="Webcam Full HD", categoria="perifericos", precio=9800.0, stock=12),
        Producto(nombre="SSD 1TB", categoria="almacenamiento", precio=18500.0, stock=25),
        Producto(nombre="RAM 16GB", categoria="componentes", precio=15600.0, stock=18),
        Producto(nombre="Mousepad XL", categoria="perifericos", precio=2100.0, stock=40),
        Producto(nombre="Hub USB-C", categoria="accesorios", precio=5400.0, stock=6, activo=False),
        Producto(nombre="Cable HDMI", categoria="accesorios", precio=1800.0, stock=50),
    ]
    session.add_all(productos)
    session.commit()


with Session(engine) as session:
    perifericos = (
        session.query(Producto)
        .filter(Producto.categoria == "perifericos")
        .all()
    )

    print("\n--- PRODUCTOS DE LA CATEGORÍA PERIFERICOS ---")
    for prod in perifericos:
        print(f"Nombre: {prod.nombre} | Precio: ${prod.precio}")


with Session(engine) as session:
    productos_caros = (
        session.query(Producto)
        .filter(Producto.precio > 10000)
        .order_by(Producto.precio.desc())
        .all()
    )

    print("\n--- PRODUCTOS MAYORES A $10000 ---")
    for prod in productos_caros:
        print(f"Nombre: {prod.nombre} | Precio: ${prod.precio}")


with Session(engine) as session:
    bajo_stock_activos = (
        session.query(Producto)
        .filter(Producto.stock <= 12, Producto.activo == True)
        .all()
    )

    print("\n--- PRODUCTOS CON STOCK <= 12 Y ACTIVOS ---")
    for prod in bajo_stock_activos:
        print(
            f"Nombre: {prod.nombre} | Stock: {prod.stock} | Activo: {prod.activo}"
        )


with Session(engine) as session:
    rango_precio = (
        session.query(Producto)
        .filter(and_(Producto.precio >= 5000, Producto.precio <= 20000))
        .all()
    )

    print("\n--- PRODUCTOS CON PRECIO ENTRE $5000 Y $20000 ---")
    for prod in rango_precio:
        print(f"Nombre: {prod.nombre} | Precio: ${prod.precio}")


with Session(engine) as session:
    mas_caro = (
        session.query(Producto)
        .order_by(Producto.precio.desc())
        .first()
    )

    print("\n--- PRODUCTO MÁS CARO DE LA TABLA ---")
    if mas_caro:
        print(f"Nombre: {mas_caro.nombre}  Precio: ${mas_caro.precio}")

#-------------------EJERCICIO-8--------------#
from sqlalchemy import Boolean, Column, Float, Integer, String, create_engine, and_
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    pass


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    categoria = Column(String)
    precio = Column(Float)
    stock = Column(Integer)
    activo = Column(Boolean, default=True)


engine = create_engine("sqlite:///:memory:", echo=False)
Base.metadata.create_all(engine)


with Session(engine) as session:
    productos = [
        Producto(nombre="Teclado mecanico", categoria="perifericos", precio=8500.0, stock=15),
        Producto(nombre="Mouse inalambrico", categoria="perifericos", precio=4200.0, stock=30),
        Producto(nombre="Monitor 24 pulgadas", categoria="monitores", precio=62000.0, stock=8),
        Producto(nombre="Auriculares bluetooth", categoria="audio", precio=12300.0, stock=20),
        Producto(nombre="Webcam Full HD", categoria="perifericos", precio=9800.0, stock=12),
        Producto(nombre="SSD 1TB", categoria="almacenamiento", precio=18500.0, stock=25),
        Producto(nombre="RAM 16GB", categoria="componentes", precio=15600.0, stock=18),
        Producto(nombre="Mousepad XL", categoria="perifericos", precio=2100.0, stock=40),
        Producto(nombre="Hub USB-C", categoria="accesorios", precio=5400.0, stock=6, activo=False),
        Producto(nombre="Cable HDMI", categoria="accesorios", precio=1800.0, stock=50),
    ]

    session.add_all(productos)
    session.commit()


with Session(engine) as session:
    perifericos = (
        session.query(Producto)
        .filter(Producto.categoria == "perifericos")
        .all()
    )

    print("\n--- PRODUCTOS DE LA CATEGORÍA PERIFERICOS ---")
    for prod in perifericos:
        print(f"Nombre: {prod.nombre}  Precio: ${prod.precio}")


with Session(engine) as session:
    productos_caros = (
        session.query(Producto)
        .filter(Producto.precio > 10000)
        .order_by(Producto.precio.desc())
        .all()
    )

    print("\n--- PRODUCTOS MAYORES A $10000 ---")
    for prod in productos_caros:
        print(f"Nombre: {prod.nombre}  Precio: ${prod.precio}")


with Session(engine) as session:
    bajo_stock_activos = (
        session.query(Producto)
        .filter(Producto.stock <= 12, Producto.activo == True)
        .all()
    )

    print("\n--- PRODUCTOS CON STOCK <= 12 Y ACTIVOS ---")
    for prod in bajo_stock_activos:
        print(
            f"Nombre: {prod.nombre}  Stock: {prod.stock}  Activo: {prod.activo}"
        )


with Session(engine) as session:
    rango_precio = (
        session.query(Producto)
        .filter(and_(Producto.precio >= 5000, Producto.precio <= 20000))
        .all()
    )

    print("\n--- PRODUCTOS CON PRECIO ENTRE $5000 Y $20000 ---")
    for prod in rango_precio:
        print(f"Nombre: {prod.nombre}  Precio: ${prod.precio}")


with Session(engine) as session:
    mas_caro = (
        session.query(Producto)
        .order_by(Producto.precio.desc())
        .first()
    )

    print("\n--- PRODUCTO MÁS CARO DE LA TABLA ---")
    if mas_caro:
        print(f"Nombre: {mas_caro.nombre}  Precio: ${mas_caro.precio}")


with Session(engine) as session:
    inactivos = (
        session.query(Producto)
        .filter(Producto.activo == False)
        .all()
    )

    print("\n--- PRODUCTOS INACTIVOS ---")
    for prod in inactivos:
        print(
            f"ID: {prod.id}  Nombre: {prod.nombre}  Activo: {prod.activo}"
        )

#------------------EJERCICIO-8-B---------------#
from sqlalchemy import Boolean, Column, Float, Integer, String, create_engine, and_
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    pass


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    categoria = Column(String)
    precio = Column(Float)
    stock = Column(Integer)
    activo = Column(Boolean, default=True)


engine = create_engine("sqlite:///:memory:", echo=False)
Base.metadata.create_all(engine)



with Session(engine) as session:
    productos = [
        Producto(nombre="Teclado mecanico", categoria="perifericos", precio=8500.0, stock=15),
        Producto(nombre="Mouse inalambrico", categoria="perifericos", precio=4200.0, stock=30),
        Producto(nombre="Monitor 24 pulgadas", categoria="monitores", precio=62000.0, stock=8),
        Producto(nombre="Auriculares bluetooth", categoria="audio", precio=12300.0, stock=20),
        Producto(nombre="Webcam Full HD", categoria="perifericos", precio=9800.0, stock=12),
        Producto(nombre="SSD 1TB", categoria="almacenamiento", precio=18500.0, stock=25),
        Producto(nombre="RAM 16GB", categoria="componentes", precio=15600.0, stock=18),
        Producto(nombre="Mousepad XL", categoria="perifericos", precio=2100.0, stock=40),
        Producto(nombre="Hub USB-C", categoria="accesorios", precio=5400.0, stock=6, activo=False),
        Producto(nombre="Cable HDMI", categoria="accesorios", precio=1800.0, stock=50),
    ]
    session.add_all(productos)
    session.commit()


with Session(engine) as session:
    perifericos = (
        session.query(Producto)
        .filter(Producto.categoria == "perifericos")
        .all()
    )

    print("\n--- PRODUCTOS DE LA CATEGORÍA PERIFERICOS ---")
    for prod in perifericos:
        print(f"Nombre: {prod.nombre}  Precio: ${prod.precio}")


with Session(engine) as session:
    productos_caros = (
        session.query(Producto)
        .filter(Producto.precio > 10000)
        .order_by(Producto.precio.desc())
        .all()
    )

    print("\n--- PRODUCTOS MAYORES A $10000 ---")
    for prod in productos_caros:
        print(f"Nombre: {prod.nombre}  Precio: ${prod.precio}")


with Session(engine) as session:
    bajo_stock_activos = (
        session.query(Producto)
        .filter(Producto.stock <= 12, Producto.activo == True)
        .all()
    )

    print("\n--- PRODUCTOS CON STOCK <= 12 Y ACTIVOS ---")
    for prod in bajo_stock_activos:
        print(
            f"Nombre: {prod.nombre}  Stock: {prod.stock}  Activo: {prod.activo}"
        )


with Session(engine) as session:
    rango_precio = (
        session.query(Producto)
        .filter(and_(Producto.precio >= 5000, Producto.precio <= 20000))
        .all()
    )

    print("\n--- PRODUCTOS CON PRECIO ENTRE $5000 Y $20000 ---")
    for prod in rango_precio:
        print(f"Nombre: {prod.nombre}  Precio: ${prod.precio}")


with Session(engine) as session:
    mas_caro = (
        session.query(Producto)
        .order_by(Producto.precio.desc())
        .first()
    )

    print("\n--- PRODUCTO MÁS CARO DE LA TABLA ---")
    if mas_caro:
        print(f"Nombre: {mas_caro.nombre}  Precio: ${mas_caro.precio}")


with Session(engine) as session:
    inactivos = (
        session.query(Producto)
        .filter(Producto.activo == False)
        .all()
    )

    print("\n--- PRODUCTOS FALSE ---")
    for prod in inactivos:
        print(
            f"ID: {prod.id}  Nombre: {prod.nombre}  Activo: {prod.activo}"
        )


with Session(engine) as session:
    hub = session.get(Producto, 9)
    if hub:
        hub.activo = True
        hub.stock = 20
        session.commit()


with Session(engine) as session:
    productos_usb = (
        session.query(Producto)
        .filter(Producto.nombre.contains("USB"))
        .all()
    )

    print("\n--- PRODUCTOS QUE CONTIENEN 'USB' EN EL NOMBRE ---")
    for prod in productos_usb:
        print(
            f"ID: {prod.id}  Nombre: {prod.nombre}  Stock: {prod.stock}  Activo: {prod.activo}"
        )

#----------------EJERCICIO-9-----------------#
from sqlalchemy import Boolean, Column, Float, Integer, String, create_engine, and_, or_
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    pass


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    categoria = Column(String)
    precio = Column(Float)
    stock = Column(Integer)
    activo = Column(Boolean, default=True)


engine = create_engine("sqlite:///:memory:", echo=False)
Base.metadata.create_all(engine)


with Session(engine) as session:
    productos = [
        Producto(nombre="Teclado mecanico", categoria="perifericos", precio=8500.0, stock=15),
        Producto(nombre="Mouse inalambrico", categoria="perifericos", precio=4200.0, stock=30),
        Producto(nombre="Monitor 24 pulgadas", categoria="monitores", precio=62000.0, stock=8),
        Producto(nombre="Auriculares bluetooth", categoria="audio", precio=12300.0, stock=20),
        Producto(nombre="Webcam Full HD", categoria="perifericos", precio=9800.0, stock=12),
        Producto(nombre="SSD 1TB", categoria="almacenamiento", precio=18500.0, stock=25),
        Producto(nombre="RAM 16GB", categoria="componentes", precio=15600.0, stock=18),
        Producto(nombre="Mousepad XL", categoria="perifericos", precio=2100.0, stock=40),
        Producto(nombre="Hub USB-C", categoria="accesorios", precio=5400.0, stock=6, activo=False),
        Producto(nombre="Cable HDMI", categoria="accesorios", precio=1800.0, stock=50),
    ]

    session.add_all(productos)
    session.commit()


with Session(engine) as session:
    perifericos = (
        session.query(Producto)
        .filter(Producto.categoria == "perifericos")
        .all()
    )

    print("\n--- PRODUCTOS DE LA CATEGORÍA PERIFERICOS ---")
    for prod in perifericos:
        print(f"Nombre: {prod.nombre}  Precio: ${prod.precio}")


with Session(engine) as session:
    productos_caros = (
        session.query(Producto)
        .filter(Producto.precio > 10000)
        .order_by(Producto.precio.desc())
        .all()
    )

    print("\n--- PRODUCTOS MAYORES A $10000 ---")
    for prod in productos_caros:
        print(f"Nombre: {prod.nombre}  Precio: ${prod.precio}")


with Session(engine) as session:
    bajo_stock_activos = (
        session.query(Producto)
        .filter(Producto.stock <= 12, Producto.activo == True)
        .all()
    )

    print("\n--- PRODUCTOS CON STOCK <= 12 Y ACTIVOS ---")
    for prod in bajo_stock_activos:
        print(
            f"Nombre: {prod.nombre}  Stock: {prod.stock}  Activo: {prod.activo}"
        )


with Session(engine) as session:
    rango_precio = (
        session.query(Producto)
        .filter(and_(Producto.precio >= 5000, Producto.precio <= 20000))
        .all()
    )

    print("\n--- PRODUCTOS CON PRECIO ENTRE $5000 Y $20000 ---")
    for prod in rango_precio:
        print(f"Nombre: {prod.nombre}  Precio: ${prod.precio}")


with Session(engine) as session:
    mas_caro = (
        session.query(Producto)
        .order_by(Producto.precio.desc())
        .first()
    )

    print("\n--- PRODUCTO MÁS CARO DE LA TABLA ---")
    if mas_caro:
        print(f"Nombre: {mas_caro.nombre}  Precio: ${mas_caro.precio}")


with Session(engine) as session:
    inactivos = (
        session.query(Producto)
        .filter(Producto.activo == False)
        .all()
    )

    print("\n--- PRODUCTOS INACTIVOS ---")
    for prod in inactivos:
        print(
            f"ID: {prod.id}  Nombre: {prod.nombre}  Activo: {prod.activo}"
        )


with Session(engine) as session:
    hub = session.get(Producto, 9)
    if hub:
        hub.activo = True
        hub.stock = 20
        session.commit()
        print("\n--- HUB USB-C ACTUALIZADO CON ÉXITO ---")


with Session(engine) as session:
    productos_usb = (
        session.query(Producto)
        .filter(Producto.nombre.contains("USB"))
        .all()
    )

    print("\n--- PRODUCTOS QUE CONTIENEN 'USB' EN EL NOMBRE ---")
    for prod in productos_usb:
        print(
            f"ID: {prod.id}  Nombre: {prod.nombre}  Stock: {prod.stock}  Activo: {prod.activo}"
        )


with Session(engine) as session:
    audio_o_componentes = (
        session.query(Producto)
        .filter(
            or_(
                Producto.categoria == "audio",
                Producto.categoria == "componentes",
            )
        )
        .all()
    )

    print("\n--- PRODUCTOS DE CATEGORÍA 'AUDIO' O 'COMPONENTES' ---")
    for prod in audio_o_componentes:
        print(
            f"Nombre: {prod.nombre}  Categoría: {prod.categoria}  Precio: ${prod.precio}"
        )

#-----------------------------EJERCICIO-10-------------------------#
from sqlalchemy import Boolean, Column, Float, Integer, String, create_engine, and_, or_
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    pass


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    categoria = Column(String)
    precio = Column(Float)
    stock = Column(Integer)
    activo = Column(Boolean, default=True)


engine = create_engine("sqlite:///:memory:", echo=False)
Base.metadata.create_all(engine)


with Session(engine) as session:
    productos = [
        Producto(nombre="Teclado mecanico", categoria="perifericos", precio=8500.0, stock=15),
        Producto(nombre="Mouse inalambrico", categoria="perifericos", precio=4200.0, stock=30),
        Producto(nombre="Monitor 24 pulgadas", categoria="monitores", precio=62000.0, stock=8),
        Producto(nombre="Auriculares bluetooth", categoria="audio", precio=12300.0, stock=20),
        Producto(nombre="Webcam Full HD", categoria="perifericos", precio=9800.0, stock=12),
        Producto(nombre="SSD 1TB", categoria="almacenamiento", precio=18500.0, stock=25),
        Producto(nombre="RAM 16GB", categoria="componentes", precio=15600.0, stock=18),
        Producto(nombre="Mousepad XL", categoria="perifericos", precio=2100.0, stock=40),
        Producto(nombre="Hub USB-C", categoria="accesorios", precio=5400.0, stock=6, activo=False),
        Producto(nombre="Cable HDMI", categoria="accesorios", precio=1800.0, stock=50),
    ]

    session.add_all(productos)
    session.commit()


with Session(engine) as session:
    perifericos = (
        session.query(Producto)
        .filter(Producto.categoria == "perifericos")
        .all()
    )

    print("\n--- PRODUCTOS DE LA CATEGORÍA PERIFERICOS ---")
    for prod in perifericos:
        print(f"Nombre: {prod.nombre} Precio: ${prod.precio}")


with Session(engine) as session:
    productos_caros = (
        session.query(Producto)
        .filter(Producto.precio > 10000)
        .order_by(Producto.precio.desc())
        .all()
    )

    print("\n--- PRODUCTOS MAYORES A $10000 ---")
    for prod in productos_caros:
        print(f"Nombre: {prod.nombre} Precio: ${prod.precio}")


with Session(engine) as session:
    bajo_stock_activos = (
        session.query(Producto)
        .filter(Producto.stock <= 12, Producto.activo == True)
        .all()
    )

    print("\n--- PRODUCTOS CON STOCK <= 12 Y ACTIVOS ---")
    for prod in bajo_stock_activos:
        print(
            f"Nombre: {prod.nombre} Stock: {prod.stock} Activo: {prod.activo}"
        )


with Session(engine) as session:
    rango_precio = (
        session.query(Producto)
        .filter(and_(Producto.precio >= 5000, Producto.precio <= 20000))
        .all()
    )

    print("\n--- PRODUCTOS CON PRECIO ENTRE $5000 Y $20000 ---")
    for prod in rango_precio:
        print(f"Nombre: {prod.nombre} Precio: ${prod.precio}")


with Session(engine) as session:
    mas_caro = (
        session.query(Producto)
        .order_by(Producto.precio.desc())
        .first()
    )

    print("\n--- PRODUCTO MÁS CARO DE LA TABLA ---")
    if mas_caro:
        print(f"Nombre: {mas_caro.nombre} Precio: ${mas_caro.precio}")


with Session(engine) as session:
    inactivos = (
        session.query(Producto)
        .filter(Producto.activo == False)
        .all()
    )

    print("\n--- PRODUCTOS INACTIVOS ---")
    for prod in inactivos:
        print(
            f"ID: {prod.id} Nombre: {prod.nombre} Activo: {prod.activo}"
        )


with Session(engine) as session:
    hub = session.get(Producto, 9)
    if hub:
        hub.activo = True
        hub.stock = 20
        session.commit()
        print("\n--- HUB USB-C ACTUALIZADO CON ÉXITO ---")


with Session(engine) as session:
    productos_usb = (
        session.query(Producto)
        .filter(Producto.nombre.contains("USB"))
        .all()
    )

    print("\n--- PRODUCTOS QUE CONTIENEN 'USB' EN EL NOMBRE ---")
    for prod in productos_usb:
        print(
            f"ID: {prod.id} Nombre: {prod.nombre} Stock: {prod.stock} Activo: {prod.activo}"
        )


with Session(engine) as session:
    audio_o_componentes = (
        session.query(Producto)
        .filter(
            or_(
                Producto.categoria == "audio",
                Producto.categoria == "componentes",
            )
        )
        .all()
    )

    print("\n--- PRODUCTOS DE CATEGORÍA 'AUDIO' O 'COMPONENTES' ---")
    for prod in audio_o_componentes:
        print(
            f"Nombre: {prod.nombre} Categoría: {prod.categoria} Precio: ${prod.precio}"
        )


with Session(engine) as session:
    productos_con_a = (
        session.query(Producto)
        .filter(Producto.nombre.contains("a"))
        .all()
    )

    cantidad = len(productos_con_a)

    print(f"\n--- PRODUCTOS QUE CONTIENEN 'a' {cantidad} EN TOTAL ---")
    for prod in productos_con_a:
        print(f"Nombre: {prod.nombre}")