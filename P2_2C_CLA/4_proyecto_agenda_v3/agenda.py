import os

def borrarPantalla():
    os.system("cls" if os.name == "nt" else "clear")

def esperarTecla():
    input("\n\t\t... Oprima cualquier tecla para continuar...")

def menu_principal():
    print("\n\t..::::: 📇 Sistema de Gestión de Agenda de Contactos 📇 :::::...\n")
    print("\t\t1️⃣ --➕ Agregar Contacto")
    print("\t\t2️⃣ --📋 Mostrar Todos los Contactos")
    print("\t\t3️⃣ --🔍 Buscar Contactos por Nombre")
    print("\t\t4️⃣ --🗑️ Eliminar Contacto")
    print("\t\t5️⃣ --✏️ Modificar Contacto")
    print("\t\t6️⃣ --❌ Salir")
    return input("\n\t\t🔹 Elige una opción (1-6): ").strip()

def agregar_contacto(agenda):
    borrarPantalla()
    print("Agregar Contacto")
    nombre = input("Nombre del contacto: ").upper().strip()
    if nombre in agenda:
        print("El contacto ya existe.")
    else:
        tel = input("Teléfono: ").strip()
        email = input("E-mail: ").strip()
        agenda[nombre] = [tel, email]
        print("Contacto agregado exitosamente.")

def mostrar_contacto(agenda):
    borrarPantalla()
    print("Mostrar Contactos")
    if not agenda:
        print("No hay contactos registrados.")
    else:
        for nombre, datos in agenda.items():
            print(f"\nNombre: {nombre}")
            print(f"Teléfono: {datos[0]}")
            print(f"E-mail: {datos[1]}")

def buscar_nombre(agenda):
    borrarPantalla()
    print("Buscar Contacto por Nombre")
    if not agenda:
        print("No hay contactos registrados.")
    else:
        nombre = input("Nombre a buscar: ").upper().strip()
        if nombre in agenda:
            print(f"\nNombre: {nombre}")
            print(f"Teléfono: {agenda[nombre][0]}")
            print(f"E-mail: {agenda[nombre][1]}")
        else:
            print("Contacto no encontrado.")

def eliminar_contacto(agenda):
    borrarPantalla()
    print("Eliminar Contactos")
    if not agenda:
        print("No hay contactos en la Agenda")
    else:
        nombre = input("Nombre del contacto a buscar: ").upper().strip()
        if nombre in agenda:
            print("Valores Actuales")
            print(f"Nombre: {nombre}\nTeléfono: {agenda[nombre][0]}\nE-mail: {agenda[nombre][1]}")
            resp = input("¿Deseas eliminar los valores? (Sí/No): ").lower().strip()
            if resp == "si":
                agenda.pop(nombre)
                print("Acción Realizada con éxito")
        else:
            print("Este contacto no existe")

def modificar_contacto(agenda):
    borrarPantalla()
    print("Modificar Contactos")
    if not agenda:
        print("No hay contactos en la Agenda")
    else:
        nombre = input("Nombre del contacto a buscar: ").upper().strip()
        if nombre in agenda:
            print("Valores Actuales")
            print(f"Nombre: {nombre}\nTeléfono: {agenda[nombre][0]}\nE-mail: {agenda[nombre][1]}")
            resp = input("¿Deseas cambiar los valores? (Sí/No): ").lower().strip()
            if resp == "si":
                tel = input("Teléfono: ").strip()
                email = input("E-mail: ").strip()
                agenda[nombre] = [tel, email]
                print("Acción Realizada con éxito")
        else:
            print("Este contacto no existe")
