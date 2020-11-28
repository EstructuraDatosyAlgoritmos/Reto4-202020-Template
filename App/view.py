"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

bikefile1 = '201801-1-citibike-tripdata.csv'
bikefile2 = '201801-2-citibike-tripdata.csv'
bikefile3 = '201801-3-citibike-tripdata.csv'
bikefile4 = '201801-4-citibike-tripdata.csv'
initialStation = None
recursionLimit =40000

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información del Citibike")
    print("3- REQ 3- Estaciones criticas")
    print("4- REQ 5- ")
    print("5- REQ 6 ")
    print("0- Salir")
    print("*******************************************")


def optionTwo():
    print("\nCargando información del citibike ....")
    controller.loadFile(cont, bikefile1)
    controller.loadFile(cont, bikefile2)
    controller.loadFile(cont, bikefile3)
    controller.loadFile(cont, bikefile4)

    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))


def optionThree():
    
    print('El top 3 de las estaciones de salida, de llegada y las menos utilizadas es: ' +
          str(controller.topStations(cont)))


def optionFour():
    print(controller.routeRecomendations(cont,ageRange))


def optionFive():
    print(controller.touristRoute(cont,lat1,lon1,lat2,lon2))
    





"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 4:
        ageRange = input("Establezca un rango de edades para las rutas recomendadas: ")
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 5:
        lat1=float(input("ingrese la latitud de inicio: "))
        lon1=float(input("ingrese la longitud de inicio: "))
        lat2=float(input("ingrese la latitud final: "))
        lon2=float(input("ingrese la longitud final: "))
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    else:
        sys.exit(0)
sys.exit(0)
