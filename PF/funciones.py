# funciones.py - Utilidades reutilizables (CORREGIDO - sin repeticiones)
import os
import sys
import time
from datetime import datetime

def limpiar_pantalla():
    """Limpia la pantalla (Windows/Linux/Mac)."""
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    """Pausa hasta que el usuario presione Enter."""
    input("Presiona Enter para continuar...")

def mostrar_titulo(titulo):
    """Muestra un título decorado."""
    print("═" * 50)
    print(f"  {titulo}")
    print("═" * 50)

def validar_opcion(min_val, max_val):
    """
    Valida una opción numérica. Muestra error y pausa.
    """
    while True:
        entrada = input(f"Elige una opción ({min_val}-{max_val}, 0 para salir): ").strip()
        if entrada == "0":
            return 0
        if not entrada.isdigit():
            print(f"❌ '{entrada}' no es un número válido.")
            pausar()
            return -1
        num = int(entrada)
        if min_val <= num <= max_val:
            return num
        else:
            print(f"❌ Opción fuera de rango. Usa entre {min_val} y {max_val}.")
            pausar()
            return -1

def validar_entrada(campo, validacion_func, mensaje_ayuda="", default=None):
    """
    Pide una entrada. Si es inválida, muestra error y pausa.
    Usa 0 para salir.
    """
    while True:
        prompt = f"{campo}"
        if default is not None:
            prompt += f" [{default}]"
        prompt += ": "
        valor = input(prompt).strip()
        if valor == "0":
            print("🔙 Operación cancelada.")
            pausar()
            return None
        if not valor and default is not None:
            return default
        if validacion_func(valor):
            return valor
        if mensaje_ayuda:
            print(f"❌ {mensaje_ayuda}")
        pausar()
        break

def formatear_fecha(fecha):
    if isinstance(fecha, str): fecha = datetime.fromisoformat(fecha)
    return fecha.strftime('%d/%m/%Y')

def formatear_moneda(monto):
    return f"$ {monto:,.2f} MXN"

def crear_tabla_ascii(titulo, headers, filas):
    """
    Crea una tabla ASCII bien formateada que se ajusta dinámicamente
    al contenido, sin exceder el ancho total de 100 caracteres.
    """
    ancho_total = 100
    num_cols = len(headers)

    # Calcular el ancho máximo de cada columna según el contenido
    anchos = []
    for i in range(num_cols):
        max_contenido = max(
            [len(str(f[i])) for f in filas] + [len(headers[i])],
            default=10
        )
        anchos.append(max(max_contenido + 2, 10))  # mínimo 10, margen de 2

    # Calcular el ancho total necesario: contenido + separadores + bordes
    # Cada columna tiene separadores: | contenido |
    # Total separadores: num_cols + 1 (uno al inicio y uno después de cada columna)
    ancho_necesario = sum(anchos) + num_cols + 1
    
    if ancho_necesario > ancho_total:
        # Reducir proporcionalmente los anchos para no pasar de ancho_total
        exceso = ancho_necesario - ancho_total
        while exceso > 0:
            for i in range(num_cols):
                if anchos[i] > 10 and exceso > 0:
                    anchos[i] -= 1
                    exceso -= 1
            if all(a <= 10 for a in anchos):
                break

    def recortar(texto, ancho):
        texto = str(texto)
        return texto if len(texto) <= ancho else texto[:ancho - 3] + "..."

    # Recalcular el ancho real después de los ajustes
    ancho_real = sum(anchos) + num_cols + 1

    # Imprimir la tabla
    print("┌" + "─" * (ancho_real - 2) + "┐")
    print(f"│ {titulo.center(ancho_real - 4)} │")
    print("├" + "─" * (ancho_real - 2) + "┤")

    # Encabezado
    encabezado = "│"
    for i, h in enumerate(headers):
        encabezado += f" {recortar(h, anchos[i] - 2).ljust(anchos[i] - 2)} │"
    print(encabezado)
    print("├" + "─" * (ancho_real - 2) + "┤")

    # Filas
    for fila in filas:
        fila_str = "│"
        for i, celda in enumerate(fila):
            valor = recortar(celda, anchos[i] - 2)
            fila_str += f" {valor.ljust(anchos[i] - 2)} │"
        print(fila_str)

    # Línea inferior
    print("└" + "─" * (ancho_real - 2) + "┘")


def validar_telefono(telefono):
    return telefono.isdigit() and len(telefono) == 10

def generar_id():
    return int(time.time())
