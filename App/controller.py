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

import config as cf
import csv
import datetime
import os
from App import model as mod

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""




# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = mod.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________


def loadTrips(citibike):
    for filename in os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            print ('Cargando archivo: ' + filename)
            loadFile(citibike,filename)
            

def loadFile(citibike, tripfile):
    tripfile= cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile,encoding="utf-8"),
                                delimiter=",")
    for trip in input_file:
        mod.addTrip(citibike,trip)
        return citibike
# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def topStations(analyzer):

    return mod.topStations(analyzer)

def routeRecomendations(analyzer,ageRange):

    return mod.routeRecomendations(analyzer,ageRange)


def touristRoute(analyzer,lat1,lon1,lat2,lon2):
    return mod.touristRoute(analyzer,lat1,lon1,lat2,lon2)
