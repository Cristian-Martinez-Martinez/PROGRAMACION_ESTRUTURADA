# main.py - Archivo principal del sistema
# 💎 JOYERÍA "ORO Y PLATA" - Sistema de Gestión
import os
import time
from datetime import datetime
from auth.usuarios import login, registro, login_admin
from funciones import *
from clientes.clientes import gestionar_clientes
from inventario.inventario import gestionar_inventario
from ventas.ventas import punto_venta

# Variables globales
usuario_actual = None

def mostrar_bienvenida():
    """Muestra la pantalla de bienvenida con logo ASCII."""
    limpiar_pantalla()
    logo = r"""
    ██████╗  █████╗ ███████╗███████╗██╗   ██╗
    ██╔══██╗██╔══██╗██╔════╝██╔════╝╚██╗ ██╔╝
    ██████╔╝███████║███████╗█████╗   ╚████╔╝ 
    ██╔══██╗██╔══██║╚════██║██╔══╝    ╚██╔╝  
    ██║  ██║██║  ██║███████║███████╗   ██║   
    ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝   
            💎 ORO Y PLATA 💎
    """
    print(logo)
    print(f"📅 Fecha: {datetime.now().strftime('%d/%m/%Y')}  ⏰ Hora: {datetime.now().strftime('%H:%M:%S')}")
    print("═" * 50)
    print("   Bienvenido al Sistema de Gestión de Joyería")
    print("═" * 50)
    pausar()

def menu_autenticacion():
    """Muestra el menú de autenticación."""
    global usuario_actual
    while True:
        limpiar_pantalla()
        mostrar_titulo("🔐 AUTENTICACIÓN")
        print("1. Iniciar Sesión")
        print("2. Registrarse")
        print("3. Modo Administrador")
        print("4. Salir del Sistema")
        print("0. 🔙 Volver")
        print("─" * 40)
        
        opcion = validar_opcion(0, 4)
        if opcion == -1:
            continue
        elif opcion == 0:
            mostrar_bienvenida()
        elif opcion == 1:
            usuario_actual = login()
            if usuario_actual:
                break
        elif opcion == 2:
            registro()
        elif opcion == 3:
            usuario_actual = login_admin()
            if usuario_actual:
                break
        elif opcion == 4:
            print("👋 ¡Hasta luego!")
            sys.exit()

def mostrar_dashboard():
    """Muestra el resumen del sistema con datos reales."""
    from conexionBD import ejecutar_query
    from funciones import formatear_moneda
    hoy = datetime.now().strftime('%Y-%m-%d')
    hora = datetime.now().strftime('%H:%M')
    
    try:
        productos = ejecutar_query("SELECT COUNT(*) as total FROM productos")[0]['total'] or 0
        clientes = ejecutar_query("SELECT COUNT(*) as total FROM clientes")[0]['total'] or 0
        ventas_hoy = ejecutar_query("""
            SELECT COALESCE(SUM(total), 0) as total 
            FROM ventas WHERE DATE(fecha) = %s
        """, (hoy,))[0]['total'] or 0.0
        ventas_hoy = float(ventas_hoy)
    except Exception:
        productos, clientes, ventas_hoy = 0, 0, 0.0

    print(f"📅 Hoy: {hoy} ⏰ {hora} 👤 Usuario: {usuario_actual['username']}")
    print(f"📊 HOY: {formatear_moneda(ventas_hoy)} | 🏷️ {productos} productos | 👥 {clientes} clientes")
    print("═" * 50)

def menu_principal():
    """Menú principal después del login."""
    global usuario_actual
    while True:
        limpiar_pantalla()
        mostrar_titulo("💎 JOYERÍA ORO Y PLATA 💎")
        mostrar_dashboard()
        print("1. 👥 GESTIÓN DE CLIENTES")
        print("2. 💎 INVENTARIO DE JOYAS")
        print("3. 🛒 PUNTO DE VENTA")
        print("4. 📊 REPORTES Y ESTADÍSTICAS")
        print("5. ⚙️ CONFIGURACIÓN")
        print("6. 🔒 CERRAR SESIÓN")
        print("7. ❌ SALIR DEL SISTEMA")
        print("═" * 50)
        
        opcion = validar_opcion(0, 7)
        if opcion == -1:
            continue
        elif opcion == 0:
            break
        elif opcion == 1:
            gestionar_clientes()
        elif opcion == 2:
            gestionar_inventario()
        elif opcion == 3:
            punto_venta()
        elif opcion == 4:
            print("📊 Reportes en desarrollo...")
            pausar()
        elif opcion == 5:
            print("⚙️ Configuración temporal...")
            pausar()
        elif opcion == 6:
            usuario_actual = None
            break
        elif opcion == 7:
            print("👋 ¡Gracias por usar el sistema!")
            sys.exit()

def main():
    """Función principal del sistema."""
    from funciones import formatear_moneda
    mostrar_bienvenida()
    while True:
        menu_autenticacion()
        while usuario_actual:
            menu_principal()

if __name__ == "__main__":
    main()
