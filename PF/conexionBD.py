# conexionBD.py - Conexión a MySQL (CORREGIDO)
import mysql.connector
from mysql.connector import Error
from funciones import mostrar_titulo

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'joyeria_oro_plata',
    'charset': 'utf8mb4',
    'autocommit': False
}

def conectar_db():
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        if conexion.is_connected():
            return conexion
        else:
            print("❌ No se pudo conectar.")
            return None
    except Error as e:
        manejar_errores_db(e)
        return None

def ejecutar_query(query, params=None):
    conexion = conectar_db()
    if not conexion: return None
    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(query, params or ())
        return cursor.fetchall()
    except Error as e:
        manejar_errores_db(e)
        return None
    finally:
        if cursor: cursor.close()
        if conexion and conexion.is_connected(): conexion.close()

def ejecutar_actualizacion(query, params=None):
    conexion = conectar_db()
    if not conexion: return False
    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute(query, params or ())
        conexion.commit()
        return True
    except Error as e:
        conexion.rollback()
        manejar_errores_db(e)
        return False
    finally:
        if cursor: cursor.close()
        if conexion and conexion.is_connected(): conexion.close()

def ejecutar_transaccion(queries_params):
    conexion = conectar_db()
    if not conexion: return None
    cursor = None
    try:
        cursor = conexion.cursor()
        for query, params in queries_params:
            cursor.execute(query, params)
        conexion.commit()
        if queries_params and queries_params[0][0].strip().upper().startswith("INSERT"):
            return cursor.lastrowid
        return True
    except Error as e:
        conexion.rollback()
        manejar_errores_db(e)
        return None
    finally:
        if cursor: cursor.close()
        if conexion and conexion.is_connected(): conexion.close()

def manejar_errores_db(error):
    print(f"❌ Error: {error}")
    if "1045" in str(error): print("→ Credenciales incorrectas.")
    elif "1049" in str(error): print("→ BD no encontrada. Ejecuta bd_proyecto.sql")
    elif "2003" in str(error): print("→ MySQL no está corriendo.")
    elif "1452" in str(error): print("→ Error de clave foránea: ID no existe.")
    else: print(f"→ Error: {error}")
