
import os
"""
  Una función es un conjunto de instrucciones agrupadas bajo un nombre en particular como un programa mas pequeño que cumple una funcion especifica. La funcion se puede reutulizar con el simple hecho de invocarla es decir mandarla llamar 

  Sintaxis:

   def nombredeMifuncion(parametros):
      bloque o conjunto de instrucciones

   nombredeMifuncion(parametros)

   Las funciones pueden ser de 4 tipos
  
    Funciones de tipo "Procedimiento" 
   1.- Funcion que no recibe parametros y no regresa valor
   3.- Funcion que recibe parametros y no regresa valor
    
    Funciones de tipo "Funcion"
   2.- Funcion que no recibe parametros y regresa valor
   4.- Funcion que recibe parametros y regresa valor

"""
os.system("cls")
    #1.- Funcion que no recibe parametros y no regresa valor
def solicitarDatos1():
    nombre = input("Nombre: ")
    telefono = input("Telefono: ")
    print(f"El nombre del contacoto es {nombre} y su telefono es {telefono}")
    #3.- Funcion que recibe parametros y no regresa valor
def solicitarDatos2(nom,tel):
    nombre = nom
    telefono = tel
    print(f"El nombre del contacoto es {nombre} y su telefono es {telefono}")
    #2.- Funcion que no recibe parametros y regresa valor
def solicitarDatos3():
    nombre = input("NOmbre: ")
    telefono = input("Telefono: ")
    return nombre, telefono
#4.- Funcion que recibe parametros y regresa valor
def solicitarDatos4(nom,tel):
    nombre = nom
    telefono = tel
    return nombre,telefono
    #Invocacion las funciones
solicitarDatos1()
nom,tel= solicitarDatos2()
print(f"\n\t :::Agenda Telefonica :::\n\t\Nombre:{nom}\n\tTelefono: {tel} ")

nombre = input("Nombre: ")
telefono = input("Telefono: ")
solicitarDatos3(nombre,telefono)

nombre = input("Nombre: ")
telefono = input("Telefono: ")
solicitarDatos4(nombre,telefono)
print(f"\n\t :::Agenda Telefonica ::: \n\t\Nombre:{nom}\n\tTelefono: {tel} ")