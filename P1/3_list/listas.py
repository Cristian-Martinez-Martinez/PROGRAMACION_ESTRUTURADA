"""Lista (Array)
Son colecciones o conjunto de datoas/valores bajo un mismo nombre, para acceder a los valores se hace con un indice numerico

Nota: sus valores si son """


import os
os.system("clear") 

#Funciones ma comunes en las listas

paises=("Mexico","Brasil","España","Canada")
numeros=[23,45,8,,24,23,56]
varios=["hola",3,1416,33,True]


#Imprimir el contenido de una lista

print(paises)
print(numeros)
print(varios)

#Recorrer un lista e imprimir el contenido
#primer forma
for i in paises :
    print(i)

Lista=""
for i in paises:
    lista=lista+f"{i},"
    print(lista)
    #2da forma
    for i in range(0,4):
        print(paises[i])


import os
#Ejmeplo 1 crear lista de numeros e imprimir contenido
os.system("clear")
numeros=[100,34]
print(numeros)

variable="{"
for i in numeros:
    variable+=f"{i}"
    print(f"{variable}")

    variable="{"
for i in range (0,len(numeros)):
    variable+=f"{numeros[i]}"
    print(f"{variable}")


   # Ejemplo 2 crear una lista de palabras y posteriormente buscar la coicidencio de una palabra

   palabras=["UTD","2023","logo","TI","2C","clasica"]
if palabra buscar in palabras:
print(("si encontro la palabra en la lista"))
else:
print("No encontro la palabra en la lista")


#3er FORMA
#=["hola","2023","Lebroncito","UTD","True","UTD"]
# encontro=False
# for i in range(0,len(palabras)):
#   if palabras[i]==palabra_buscar:
#     encontro=True 
    
# if encontro:
#   print("SI se encontro la palabra en la lista")
# else:
#     print("NO se encontro la palabra en la lista")  

#Ejemplo 3 Añadir elementos a la lista
os.system("clear")
# numeros=[]

# opc="si"
# while opc=="si":
#    numeros.append(float(input("Dame un numero entero o decimal: ")))
#    opc=input("¿Desear agregar otro numero a las lista (si/no)? ").lower()
# print(numeros)   






#Ejemplo 4 Crear una lista multidimensional de numerospara almacenar los nombres y telefonos de uno contactos "nombres" y "telefonos"agemda"
aagenda=[
        ["Carlos","6181234567"],
        ["Alberto","6671234567"],
        ["Martin","6785678923"]
       ]

print(agenda)

for i in agenda:
    print(i)

for r in range(0,3):
    for c in range(0,2):
        print(agenda[r][c])    

cadena=""
for r in range(0,3):
    for c in range(0,2):
      cadena+=f"{agenda[r][c]}, "
    cadena+="\n"     
print(cadena) 