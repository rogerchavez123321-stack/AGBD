import os
import mysql.connector
from dotenv import load_dotenv

from pathlib import Path
load_dotenv(Path(__file__).resolve().parent / ".env")

try:
    conexion = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    if conexion.is_connected():
        print("Conexión exitosa con Stock-Controler")

except mysql.connector.Error as error:
    print(f"Error de conexión: {error}")

finally:
    if "conexion" in locals() and conexion.is_connected():
        conexion.close()