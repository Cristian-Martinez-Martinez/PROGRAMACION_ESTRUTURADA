
import os
#Ejemplo 1 crear un lista de numeros e imprimir el contenido

os.system("cls")
numeros =[100,34]
print(numeros)

variable="["
for i in numeros:
    variable+=f"{i}"
print(f"{variable}]")


variable="["
for i in range(0,len(numeros)):
    variable+=f"{numeros[i]}, "
print(f"{variable}]")

#Ejemplo 2 crear una lista de palabra y posteriormente buecar la coincidencia de una palabra
os.system("cls")

palabras=["UTD", "2023","logo","TI","2C","clasica"]
print(palabras)
palabras_buscar=input("Dame la palabra a buscar en la lista: ")

#1er forma
if palabras_buscar in palabras:
    print("Si encontro la palabra en la lista")
else:
    print("No encontro la palabra en la lista")

#2da forma
for i in palabras:
    if i==palabras_buscar:
        print("Si encontro la palabra en la lista")
    else:
        print("No encontro la palabra en la lista")
        ''' ejemplo de como sale la trminal si un valos no se encuentra
            no encontro en la lista
            no encontro en la lista
            no encontro en la lisat 
            no encontro en la lista'''

#un ejemplo mas
encontro=False
cuantas=0
posicion=[]
for i in palabras:
    if i==palabras_buscar:
        encontro=True
        cuantas+=1
        posicion.append(palabras.index(i))
if encontro:
    print("Si se encontro la palabra en la lista")
else:
    print("No se encontro en la lista")

#3er forma
encontro=False
cuantas=0
posicion=[]
for i in range(0,len(palabras)):
    if i==palabras_buscar:
        encontro=True
        cuantas+=1
        posicion.append(palabras.index(i))
if encontro:
    print("Si se encontro la palabra en la lista")
else:
    print("No se encontro en la lista")
#Ejemplo 4 cerar un lista multidimensional para almacenar lo nombres y los telefonos de unos contactos "agenda"
    
agenda=[
        ["Carlos", "6181234567"],
        ["Carlos V", "6181234568"],
        ["Carlos VI", "6187894562"],
        ]
print(agenda)
for i in agenda:
    print(i)

for r in range(0,3):
    for c in range(0,2):
        print([r][c])

for r in range(0,3):
    for c in range(0,2):
        lista+=f"{agenda[r][c]}, "
    lista+="\n"