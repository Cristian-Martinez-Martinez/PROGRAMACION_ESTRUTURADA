# auth/usuarios.py - Gestión de usuarios y autenticación
from conexionBD import ejecutar_query, ejecutar_actualizacion, manejar_errores_db
from funciones import *
import re
import getpass
import hashlib

def hash_password(password):
    """Encripta la contraseña usando SHA256."""
    return hashlib.sha256((password + "oro_plata_salt").encode('utf-8')).hexdigest()

def validar_email(email):
    return re.match(r'^[^@]+@[^@]+\.[^@]+$', email) is not None

def validar_usuario(usuario):
    return re.match(r'^[a-zA-Z0-9_]{3,50}$', usuario) is not None

def login():
    limpiar_pantalla()
    mostrar_titulo("🔐 INICIAR SESIÓN")
    username = input("Usuario: ").strip()
    if not username:
        print("❌ El usuario es obligatorio.")
        pausar()
        return None
    password = getpass.getpass("Contraseña: ")
    if not password:
        print("❌ La contraseña es obligatoria.")
        pausar()
        return None

    pwd_hash = hash_password(password)
    query = "SELECT id, username, tipo FROM usuarios WHERE username = %s AND password_hash = %s"
    try:
        resultado = ejecutar_query(query, (username, pwd_hash))
        if resultado:
            print(f"✅ Bienvenido, {resultado[0]['username']}!")
            pausar()
            return {'id': resultado[0]['id'], 'username': resultado[0]['username'], 'tipo': resultado[0]['tipo']}
        else:
            print("❌ Usuario o contraseña incorrectos.")
            pausar()
            return None
    except Exception as e:
        manejar_errores_db(e)
        pausar()
        return None

def registro():
    limpiar_pantalla()
    mostrar_titulo("📝 REGISTRARSE")
    username = validar_entrada("Nombre de usuario", validar_usuario, "Solo letras, números y _ (3-50)")
    if username is None: return
    email = validar_entrada("Email", validar_email, "Formato: usuario@dominio.com")
    if email is None: return
    password = getpass.getpass("Contraseña: ")
    confirm = getpass.getpass("Confirmar contraseña: ")
    if password != confirm:
        print("❌ Las contraseñas no coinciden.")
        pausar()
        return
    
    pwd_hash = hash_password(password)
    query = "INSERT INTO usuarios (username, email, password_hash) VALUES (%s, %s, %s)"
    try:
        if ejecutar_actualizacion(query, (username, email, pwd_hash)):
            print(f"✅ Usuario '{username}' registrado exitosamente.")
        else:
            print("❌ No se pudo registrar.")
    except Exception as e:
        if "Duplicate entry" in str(e):
            print("❌ El usuario o email ya existe.")
        else:
            manejar_errores_db(e)
    pausar()

def login_admin():
    limpiar_pantalla()
    mostrar_titulo("👑 MODO ADMINISTRADOR")
    clave = getpass.getpass("Clave maestra: ")
    if clave == "admin_oro_plata":
        print("✅ Acceso como administrador concedido.")
        pausar()
        return {'id': 1, 'username': 'admin', 'tipo': 'admin'}
    else:
        print("❌ Clave incorrecta.")
        pausar()
        return None
