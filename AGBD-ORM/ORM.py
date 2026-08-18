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