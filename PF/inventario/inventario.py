# inventario/inventario.py - Gestión de inventario
from conexionBD import ejecutar_query, ejecutar_actualizacion, manejar_errores_db
from funciones import *

CATEGORIAS = ['anillos', 'collares', 'aretes', 'relojes', 'pulseras', 'piedras']

def agregar_producto():
    limpiar_pantalla()
    mostrar_titulo("➕ AGREGAR PRODUCTO")
    nombre = input("Nombre del producto: ").strip()
    if not nombre:
        print("❌ El nombre del producto es obligatorio.")
        pausar()
        return
    categoria = input("Categoría (anillos, collares, etc.): ").strip()
    if categoria not in CATEGORIAS:
        print(f"❌ Categoría inválida. Usa: {', '.join(CATEGORIAS)}")
        pausar()
        return
    precio_input = input("Precio: ").strip()
    if not precio_input.replace('.', '').isdigit():
        print("❌ Ingresa un número válido para el precio.")
        pausar()
        return
    precio = float(precio_input)
    stock_input = input("Stock inicial: ").strip()
    if not stock_input.isdigit():
        print("❌ Ingresa un número entero para el stock.")
        pausar()
        return
    stock = int(stock_input)
    descripcion = input("Descripción (opcional): ").strip() or None

    query = """INSERT INTO productos (nombre, categoria, precio, stock, descripcion) 
               VALUES (%s, %s, %s, %s, %s)"""
    if ejecutar_actualizacion(query, (nombre, categoria, precio, stock, descripcion)):
        print("✅ Producto agregado.")
    else:
        print("❌ Error al guardar.")
    pausar()

def mostrar_inventario():
    limpiar_pantalla()
    mostrar_titulo("📦 INVENTARIO COMPLETO")
    query = "SELECT id, nombre, categoria, precio, stock, descripcion FROM productos"
    try:
        productos = ejecutar_query(query)
        if productos:
            headers = ["ID", "Nombre", "Categoría", "Precio", "Stock", "Descripción"]
            filas = [[p['id'], p['nombre'], p['categoria'], formatear_moneda(p['precio']), 
                     p['stock'], (p['descripcion'] or "-")[:30]] for p in productos]
            crear_tabla_ascii("Inventario", headers, filas)
        else:
            print("No hay productos.")
    except Exception as e:
        manejar_errores_db(e)
    pausar()

def productos_bajo_stock():
    limpiar_pantalla()
    mostrar_titulo("⚠️ PRODUCTOS BAJO STOCK")
    limite_input = input("Límite de stock bajo (Enter para usar 5): ").strip()
    if not limite_input:
        limite = 5
    elif limite_input.isdigit():
        limite = int(limite_input)
    else:
        print("❌ Ingresa un número válido.")
        pausar()
        return

    query = "SELECT * FROM productos WHERE stock <= %s"
    try:
        productos = ejecutar_query(query, (limite,))
        if productos:
            headers = ["ID", "Nombre", "Stock", "Precio"]
            filas = [[p['id'], p['nombre'], p['stock'], formatear_moneda(p['precio'])] for p in productos]
            crear_tabla_ascii(f"Stock ≤ {limite}", headers, filas)
        else:
            print("🟢 Todo el inventario está por encima del límite.")
    except Exception as e:
        manejar_errores_db(e)
    pausar()

def calcular_valor_total():
    query = "SELECT SUM(precio * stock) as total FROM productos"
    try:
        total = ejecutar_query(query)[0]['total'] or 0
        print(f"💰 Valor total: {formatear_moneda(total)}")
    except Exception as e:
        manejar_errores_db(e)
    pausar()

def actualizar_precios():
    limpiar_pantalla()
    mostrar_titulo("💰 ACTUALIZAR PRECIOS")
    
    # Validar entrada
    porcentaje_str = validar_entrada(
        "Porcentaje de aumento",
        lambda x: x.replace('.', '').isdigit(),
        "Solo números positivos (ej: 10, 5.5)"
    )
    
    # Si el usuario canceló (presionó 0)
    if porcentaje_str is None:
        return  # Vuelve al menú sin hacer nada

    try:
        porcentaje = float(porcentaje_str)
        if porcentaje < 0:
            print("❌ El porcentaje no puede ser negativo.")
            pausar()
            return
    except ValueError:
        print("❌ Ingresa un número válido.")
        pausar()
        return

    # Confirmar acción
    if input(f"Aumentar precios en {porcentaje}%? (s/n): ").lower() != 's':
        print("Operación cancelada.")
        pausar()
        return

    # Ejecutar actualización
    if ejecutar_actualizacion("UPDATE productos SET precio = precio * (1 + %s/100)", (porcentaje,)):
        print(f"✅ Precios actualizados en {porcentaje}%.")
    else:
        print("❌ Error al actualizar precios.")
    pausar()

def buscar_por_categoria():
    limpiar_pantalla()
    mostrar_titulo("🔍 FILTRAR POR CATEGORÍA")
    print("Categorías disponibles:", ', '.join(CATEGORIAS))
    categoria = input("Categoría: ").strip()
    if not categoria:
        print("❌ Debes seleccionar una categoría.")
        pausar()
        return
    if categoria not in CATEGORIAS:
        print(f"❌ Categoría inválida. Usa: {', '.join(CATEGORIAS)}")
        pausar()
        return

    query = "SELECT * FROM productos WHERE categoria = %s"
    try:
        productos = ejecutar_query(query, (categoria,))
        if productos:
            headers = ["ID", "Nombre", "Precio", "Stock"]
            filas = [[p['id'], p['nombre'], formatear_moneda(p['precio']), p['stock']] for p in productos]
            crear_tabla_ascii(f"{categoria.title()}", headers, filas)
        else:
            print(f"🟢 No hay productos en la categoría '{categoria}'.")
    except Exception as e:
        manejar_errores_db(e)
    pausar()

def reporte_inventario():
    limpiar_pantalla()
    mostrar_titulo("📈 REPORTE DE INVENTARIO")
    try:
        total = ejecutar_query("SELECT COUNT(*) as total FROM productos")[0]['total']
        unidades = ejecutar_query("SELECT SUM(stock) as unidades FROM productos")[0]['unidades'] or 0
        promedio = ejecutar_query("SELECT AVG(precio) as promedio FROM productos")[0]['promedio'] or 0
        categorias = ejecutar_query("SELECT categoria, COUNT(*) as cant FROM productos GROUP BY categoria")
        
        print(f"📊 Total: {total}")
        print(f"📦 Unidades: {unidades}")
        print(f"💰 Precio promedio: {formatear_moneda(promedio)}")
        print(f"🗂️ Distribución:")
        for c in categorias:
            print(f"  - {c['categoria'].title()}: {c['cant']}")
        calcular_valor_total()
    except Exception as e:
        manejar_errores_db(e)
    pausar()

def gestionar_inventario():
    while True:
        limpiar_pantalla()
        mostrar_titulo("💎 INVENTARIO DE JOYAS")
        print("1. ➕ Agregar nuevo producto")
        print("2. 📦 Ver inventario completo")
        print("3. 🔍 Buscar por categoría")
        print("4. ⚠️ Productos bajo stock")
        print("5. 💰 Actualizar precios")
        print("6. 📊 Valor total del inventario")
        print("7. 📈 Generar reporte")
        print("0. 🔙 Volver")
        print("─" * 40)
        
        opcion = validar_opcion(0, 7)
        if opcion == -1:
            continue
        elif opcion == 0:
            return
        elif opcion == 1:
            agregar_producto()
        elif opcion == 2:
            mostrar_inventario()
        elif opcion == 3:
            buscar_por_categoria()
        elif opcion == 4:
            productos_bajo_stock()
        elif opcion == 5:
            actualizar_precios()
        elif opcion == 6:
            calcular_valor_total()
        elif opcion == 7:
            reporte_inventario()
