# ventas/ventas.py - Sistema de ventas (POS)
from conexionBD import ejecutar_query, ejecutar_actualizacion, ejecutar_transaccion, manejar_errores_db
from funciones import *
from decimal import Decimal
from datetime import datetime

METODOS_PAGO = ['efectivo', 'tarjeta', 'transferencia']
DESCUENTOS = {'temporada': Decimal('0.10')}

def nueva_venta():
    limpiar_pantalla()
    mostrar_titulo("🆕 NUEVA VENTA")
    cliente_id = None
    busqueda = input("Buscar cliente (0 para anónimo): ").strip()
    if busqueda == "0": pass
    elif busqueda:
        clientes = ejecutar_query("SELECT id, nombre FROM clientes WHERE nombre LIKE %s OR telefono LIKE %s", (f'%{busqueda}%', f'%{busqueda}%'))
        if clientes:
            print("\nClientes:")
            for c in clientes: print(f"  {c['id']}. {c['nombre']}")
            cid = validar_entrada("ID cliente", lambda x: x.isdigit() or x=='', "0 para anónimo")
            cliente_id = int(cid) if cid else None
        else:
            print("🔍 No encontrado. Venta anónima.")
            pausar()

    carrito = []
    while True:
        prod_nombre = input("\nNombre del producto (fin para terminar, 0 para cancelar): ").strip()
        if prod_nombre.lower() == '0': return
        if prod_nombre.lower() == 'fin': break
        productos = ejecutar_query("SELECT id, nombre, precio, stock FROM productos WHERE nombre LIKE %s", (f'%{prod_nombre}%',))
        if not productos:
            print("❌ No encontrado.")
            continue
        print("\nProductos:")
        for p in productos: print(f"  {p['id']}. {p['nombre']} - {formatear_moneda(p['precio'])} (Stock: {p['stock']})")
        
        try:
            pid = int(input("\nID del producto: "))
            producto = next((p for p in productos if p['id'] == pid), None)
            if not producto:
                print("❌ ID inválido.")
                continue
            max_cant = producto['stock']
            cant = int(input(f"Cantidad (máx {max_cant}): "))
            if cant <= 0 or cant > max_cant:
                print(f"❌ Rango: 1-{max_cant}.")
                continue
            subtotal = producto['precio'] * Decimal(cant)
            carrito.append({'id': pid, 'nombre': producto['nombre'], 'precio': producto['precio'], 'cantidad': cant, 'subtotal': subtotal})
            print(f"✅ {cant} x {producto['nombre']} = {formatear_moneda(subtotal)}")
        except:
            print("❌ Ingresa un número válido.")

    if not carrito:
        print("\n🛒 Vacío.")
        pausar()
        return

    subtotal = sum(item['subtotal'] for item in carrito)
    descuento = aplicar_descuentos(subtotal)
    impuestos = subtotal * Decimal('0.16')
    total = subtotal - descuento + impuestos

    print(f"\n🧾 Subtotal:     {formatear_moneda(subtotal)}")
    if descuento > 0: print(f"   Descuento:    -{formatear_moneda(descuento)}")
    print(f"   Impuestos:    +{formatear_moneda(impuestos)}")
    print(f"   📦 Total:     {formatear_moneda(total)}")

    metodo = validar_entrada("Método de pago", lambda x: x in METODOS_PAGO, f"{METODOS_PAGO}")
    if metodo is None: return

    if input("\n¿Confirmar venta? (s/n): ").lower() != 's':
        print("Cancelada.")
        pausar()
        return

    try:
        venta_id = ejecutar_transaccion([
            ("INSERT INTO ventas (cliente_id, subtotal, descuento, impuestos, total, metodo_pago) VALUES (%s, %s, %s, %s, %s, %s)",
             (cliente_id, float(subtotal), float(descuento), float(impuestos), float(total), metodo))
        ])
        if not venta_id:
            print("❌ Error al registrar venta.")
            pausar()
            return

        for item in carrito:
            ejecutar_actualizacion(
                "INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario, subtotal) VALUES (%s, %s, %s, %s, %s)",
                (venta_id, item['id'], item['cantidad'], float(item['precio']), float(item['subtotal']))
            )
            ejecutar_actualizacion(
                "UPDATE productos SET stock = stock - %s WHERE id = %s",
                (item['cantidad'], item['id'])
            )
        generar_factura(venta_id, carrito, subtotal, descuento, impuestos, total, metodo)
    except Exception as e:
        manejar_errores_db(e)
    pausar()

def aplicar_descuentos(subtotal):
    desc = Decimal('0.0')
    if subtotal > Decimal('5000'): desc += subtotal * DESCUENTOS['temporada']
    return desc

def generar_factura(venta_id, carrito, subtotal, descuento, impuestos, total, metodo):
    print("\n" + "="*50)
    print("           💎 JOYERÍA ORO Y PLATA 💎")
    print("               FACTURA DE VENTA")
    print("="*50)
    print(f"Folio: {venta_id}")
    print(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("-"*50)
    for item in carrito:
        print(f"{item['cantidad']}x {item['nombre']}")
        print(f"    {formatear_moneda(item['precio'])} x {item['cantidad']} = {formatear_moneda(item['subtotal'])}")
    print("-"*50)
    print(f"Subtotal:     {formatear_moneda(subtotal)}")
    if descuento > 0: print(f"Descuento:    -{formatear_moneda(descuento)}")
    print(f"Impuestos:    +{formatear_moneda(impuestos)}")
    print(f"Total:        {formatear_moneda(total)}")
    print(f"Método:       {metodo.title()}")
    print("\n¡Gracias!")
    print("="*50)

def ventas_del_dia():
    fecha = datetime.now().strftime('%Y-%m-%d')
    ventas = ejecutar_query("""SELECT v.id, c.nombre, v.total, v.metodo_pago 
                               FROM ventas v LEFT JOIN clientes c ON v.cliente_id = c.id 
                               WHERE DATE(v.fecha) = %s""", (fecha,))
    if ventas:
        from funciones import crear_tabla_ascii
        crear_tabla_ascii(f"Ventas del día: {fecha}", ["Folio", "Cliente", "Total", "Método"],
                         [[v['id'], v['nombre'] or "Anónimo", formatear_moneda(v['total']), v['metodo_pago']] for v in ventas])
    else:
        print("No hay ventas hoy.")
    pausar()

def punto_venta():
    while True:
        limpiar_pantalla()
        mostrar_titulo("🛒 PUNTO DE VENTA")
        print("1. 🆕 Nueva venta")
        print("2. 🧾 Ver ventas del día")
        print("3. 🔍 Buscar venta por folio")
        print("4. 💳 Métodos de pago")
        print("5. 🎁 Gestionar descuentos")
        print("6. 📊 Reportes de ventas")
        print("0. 🔙 Volver")
        print("─" * 40)
        opcion = validar_opcion(0, 6)
        if opcion == -1:
            continue
        elif opcion == 0: return
        elif opcion == 1: nueva_venta()
        elif opcion == 2: ventas_del_dia()
        elif opcion == 3: print("🔍 No implementado."); pausar()
        elif opcion == 4: print("💳:", ', '.join(METODOS_PAGO)); pausar()
        elif opcion == 5: print("🎁:", ', '.join(f"{k}({v*100:.0f}%)" for k,v in DESCUENTOS.items())); pausar()
        elif opcion == 6: print("📊 En desarrollo..."); pausar()
