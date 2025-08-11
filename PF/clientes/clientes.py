# clientes/clientes.py - Gestión de clientes
from conexionBD import ejecutar_query, ejecutar_actualizacion, manejar_errores_db
from funciones import  *
import csv

def agregar_cliente():
    limpiar_pantalla()
    mostrar_titulo("➕ AGREGAR CLIENTE")
    nombre = input("Nombre: ").strip()
    if not nombre:
        print("❌ El nombre es obligatorio.")
        pausar()
        return
    telefono = input("Teléfono (10 dígitos): ").strip()
    if not telefono.isdigit() or len(telefono) != 10:
        print("❌ Teléfono inválido. Usa 10 dígitos.")
        pausar()
        return
    email = input("Email (opcional): ").strip()
    email = email if email else None
    direccion = input("Dirección (opcional): ").strip()
    direccion = direccion if direccion else None

    query = """INSERT INTO clientes (nombre, telefono, email, direccion) VALUES (%s, %s, %s, %s)"""
    try:
        if ejecutar_actualizacion(query, (nombre, telefono, email, direccion)):
            print(f"✅ Cliente '{nombre}' agregado.")
        else:
            print("❌ Error al guardar.")
    except Exception as e:
        manejar_errores_db(e)
    pausar()

def buscar_cliente():
    """
    Muestra todos los clientes o busca por término.
    Ahora combina 'ver todos' y 'buscar' en una sola función.
    """
    limpiar_pantalla()
    mostrar_titulo("🔍 BUSCAR Y VER CLIENTES")
    termino = input("Buscar (nombre, teléfono o ID, Enter para ver todos): ").strip()

    if termino == "":
        query = "SELECT id, nombre, telefono, email, direccion, fecha_registro FROM clientes"
        params = None
    else:
        query = """SELECT id, nombre, telefono, email, direccion, fecha_registro 
                   FROM clientes WHERE nombre LIKE %s OR telefono LIKE %s OR CAST(id AS CHAR) = %s"""
        params = [f'%{termino}%', f'%{termino}%', termino]

    try:
        resultados = ejecutar_query(query, params)
        if resultados:
            headers = ["ID", "Nombre", "Teléfono", "Email", "Dirección", "Registro"]
            filas = [
                [c['id'], c['nombre'], c['telefono'], c['email'] or "-", 
                 c['direccion'] or "-", formatear_fecha(c['fecha_registro'])]
                for c in resultados
            ]
            crear_tabla_ascii("Resultados", headers, filas)
        else:
            print("🔍 No se encontraron clientes.")
    except Exception as e:
        manejar_errores_db(e)
    pausar()

def editar_cliente():
    id_cliente = validar_entrada("ID del cliente a editar", lambda x: x.isdigit(), "Solo números")
    if id_cliente is None: return
    cliente = ejecutar_query("SELECT * FROM clientes WHERE id = %s", (id_cliente,))
    if not cliente:
        print("❌ Cliente no encontrado.")
        pausar()
        return
    c = cliente[0]
    datos = {'id': id_cliente}

    nombre = validar_entrada("Nuevo nombre", lambda x: len(x) > 0, default=c['nombre'])
    if nombre is None: return
    datos['nombre'] = nombre

    telefono = validar_entrada("Nuevo teléfono", lambda x: x.isdigit() and len(x) == 10, default=c['telefono'])
    if telefono is None: return
    datos['telefono'] = telefono

    email = input(f"Nuevo email [{c['email']}]: ").strip() or c['email']
    direccion = input(f"Dirección [{c['direccion']}]: ").strip() or c['direccion']
    datos['email'] = email
    datos['direccion'] = direccion
    
    query = """UPDATE clientes SET nombre=%s, telefono=%s, email=%s, direccion=%s WHERE id=%s"""
    try:
        ejecutar_actualizacion(query, (datos['nombre'], datos['telefono'], datos['email'], datos['direccion'], id_cliente))
        print("✅ Cliente actualizado.")
    except Exception as e:
        manejar_errores_db(e)
    pausar()

def eliminar_cliente():
    id_cliente = validar_entrada("ID del cliente a eliminar", lambda x: x.isdigit(), "Solo números")
    if id_cliente is None: return
    cliente = ejecutar_query("SELECT nombre FROM clientes WHERE id = %s", (id_cliente,))
    if not cliente:
        print("❌ Cliente no encontrado.")
        pausar()
        return
    confirmar = input(f"¿Eliminar a {cliente[0]['nombre']}? (s/n, 0 para cancelar): ").lower()
    if confirmar == '0': return
    if confirmar == 's':
        try:
            ejecutar_actualizacion("DELETE FROM clientes WHERE id = %s", (id_cliente,))
            print("🗑️ Cliente eliminado.")
        except Exception as e:
            manejar_errores_db(e)
    else:
        print("Operación cancelada.")
    pausar()

def exportar_clientes_csv():
    query = "SELECT * FROM clientes"
    try:
        clientes = ejecutar_query(query)
        if clientes:
            filename = f"clientes_{generar_id()}.csv"
            with open(filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(clientes[0].keys())
                for c in clientes:
                    writer.writerow(c.values())
            print(f"📁 Exportado a {filename}")
        else:
            print("No hay clientes.")
    except Exception as e:
        print(f"❌ Error: {e}")
    pausar()

def gestionar_clientes():
    while True:
        limpiar_pantalla()
        mostrar_titulo("👥 GESTIÓN DE CLIENTES")
        print("1. ➕ Agregar nuevo cliente")
        print("2. 🔍 Buscar y ver clientes")
        print("3. ✏️ Editar cliente")
        print("4. 🗑️ Eliminar cliente")
        print("5. 📁 Exportar a CSV")
        print("0. 🔙 Volver")
        print("─" * 40)
        
        opcion = validar_opcion(0, 5)
        if opcion == 0:
            return
        elif opcion == 1:
            agregar_cliente()
        elif opcion == 2:
            buscar_cliente()
        elif opcion == 3:
            editar_cliente()
        elif opcion == 4:
            eliminar_cliente()
        elif opcion == 5:
            exportar_clientes_csv()