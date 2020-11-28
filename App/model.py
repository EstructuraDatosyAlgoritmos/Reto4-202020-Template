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


"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""




import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import dfs as dfs
from DISClib.Utils import error as error
from DISClib.DataStructures import edge as e
from DISClib.ADT import orderedmap as om
from DISClib.ADT import stack
from DISClib.DataStructures import mapentry as me
from math import radians, cos, sin, asin, sqrt
import datetime 
import time
assert config


#Esta es la estructura que debes usar para que todo funcione

def newAnalyzer():
    try:
        citibike = {
                    'graph': None,
                    'stations': None,
                    'exitStations':None,
                    'arriveStations':None,
                    'totalStations':None,   
                    'paths':None          
                    }

        citibike['graph']=gr.newGraph(datastructure='ADJ_LIST',
                                        directed=True,
                                        size=1000,
                                        comparefunction=compareStations)
        citibike['exitStations']=m.newMap(1019,
                                        maptype='PROBING',
                                        loadfactor=0.5,
                                        comparefunction=compareStations)
        citibike['arriveStations']=m.newMap(1019,
                                        maptype='PROBING',
                                        loadfactor=0.5,
                                        comparefunction=compareStations)
        citibike['totalStations']=m.newMap(1019,
                                        maptype='PROBING',
                                        loadfactor=0.5,
                                        comparefunction=compareStations)                                  
        citibike['stations']=lt.newList('ARRAY_LIST', compareStations)
        return citibike

    except Exception as exp:
        error.reraise(exp,'model:newAnalyzer')


#Funciones para cargar los datos a la estructura

def addTrip(citibike, trip):
    """
    """
    lst=citibike['stations']
    origin = trip['start station id']
    destination = trip['end station id']
    duration = int(trip['tripduration'])
    addStation(citibike,origin)
    addStation(citibike,destination)
    addStartStation(citibike,origin)
    addArriveStation(citibike,destination)
    addTotalStation(citibike,origin)
    addTotalStation(citibike,destination)
    addConnection(citibike,origin,destination,duration)
    lt.addLast(lst,trip)


def addStation(citibike,stationId):
    """
    Adiciona una estación como un vértice del grafo
    """
    if not gr.containsVertex(citibike['graph'],stationId):
        gr.insertVertex(citibike['graph'],stationId)
    return citibike

def addConnection(citibike,start,finish,duration):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(citibike['graph'],start,duration)
    if edge is None:
        gr.addEdge(citibike['graph'],start,finish,duration)
    else:
        e.updateAverageWeight(edge,duration)
    return citibike

def newStartStation(station):
    """
    Crea una nueva estructura para modelar los viajes de una estación
    """
    startStation = {'name': '', 'trips':0}
    startStation['name'] = station
    return startStation

def addStartStation(citibike,station):
    """
    Crea una nueva estructura para modelar los viajes de una estación
    """
    startStations = citibike['exitStations']
    existStation = m.contains(startStations,station)
    if existStation:
        entry = m.get(startStations,station)
        data = me.getValue(entry)
    else:
        data = newStartStation(station)
        m.put(startStations,station,data)
    data['trips'] +=1

def newArriveStation(station):
    """
    Crea una nueva estructura para modelar los viajes de una estación
    """
    arriveStation = {'name': '', 'trips':0}
    arriveStation['name'] = station
    return arriveStation

def addArriveStation(citibike,station):
    """
    Crea una nueva estructura para modelar los viajes de una estación
    """
    arriveStations = citibike['arriveStations']
    existStation = m.contains(arriveStations,station)
    if existStation:
        entry = m.get(arriveStations,station)
        data = me.getValue(entry)
    else:
        data = newArriveStation(station)
        m.put(arriveStations,station,data)
    data['trips'] +=1

def newTotalStation(station):
    """
    Crea una nueva estructura para modelar los viajes de una estación
    """
    totalStation = {'name': '', 'trips':0}
    totalStation['name'] = station
    return totalStation

def addTotalStation(citibike,station):
    """
    Crea una nueva estructura para modelar los viajes de una estación
    """
    totalStations = citibike['totalStations']
    existStation = m.contains(totalStations,station)
    if existStation:
        entry = m.get(totalStations,station)
        data = me.getValue(entry)
    else:
        data = newTotalStation(station)
        m.put(totalStations,station,data)
    data['trips'] +=1



########## REQUERIMIENTO 3 #############
def topStations(citibike):
    """
    Da la información de:
    - Top 3 estaciones de llegada
    - Top 3 estaciones de salida
    - Top 3 estaciones menos utilizadas
    """
    lstExit = lt.newList("ARRAY_LIST")
    lstArrive = lt.newList("ARRAY_LIST")
    lstTotal = lt.newList("ARRAY_LIST")
    count = 0
    while count < 3:
        obtainValues(citibike,lstExit,'e') #Se obtienen las estaciones con más salidas
        obtainValues(citibike,lstArrive,'a') #Se obtienen las estaciones con más llegadas
        obtainValues(citibike,lstTotal,'t') #Se obtienen las estaciones menos usadas
        count += 1

    pos = 1
    while pos < 4:       #Se intercambia el ID por el nombre correspondiente de la estación
        changeInfo(citibike,lstExit,pos)
        changeInfo(citibike,lstArrive,pos)
        changeInfo(citibike,lstTotal,pos)
        pos+=1

    #Se obtienen los resultados finales    
    eM1 = lt.getElement(lstExit,1)
    eM2 = lt.getElement(lstExit,2)
    eM3 = lt.getElement(lstExit,3)
    aM1 = lt.getElement(lstArrive,1)
    aM2 = lt.getElement(lstArrive,2)
    aM3 = lt.getElement(lstArrive,3)
    tM1 = lt.getElement(lstTotal,1)
    tM2 = lt.getElement(lstTotal,2)
    tM3 = lt.getElement(lstTotal,3)

    return eM1,eM2,eM3,aM1,aM2,aM3,tM1,tM2,tM3

#Las dos de abajo son funciones helper
def obtainValues(citibike,lst,method):
    """
    Agrega los ID de las estaciones a su lista correspondiente
    """
    if method == 'e':
        exitValues = m.valueSet(citibike['exitStations'])
        stationId = ''
        value = 0
        iterator = it.newIterator(exitValues)
        while it.hasNext(iterator):
            info = it.next(iterator)
            if info['trips'] > value:
                value = info['trips']
                stationId = info['name']
        m.remove(citibike['exitStations'],stationId)
        lt.addLast(lst,stationId)
    elif method == 'a':
        arriveValues = m.valueSet(citibike['arriveStations'])
        stationId = ''
        value = 0
        iterator = it.newIterator(arriveValues)
        while it.hasNext(iterator):
            info = it.next(iterator)
            if info['trips'] > value:
                value = info['trips']
                stationId = info['name']
        m.remove(citibike['arriveStations'],stationId)
        lt.addLast(lst,stationId)
    elif method == 't':
        totalValues = m.valueSet(citibike['totalStations'])
        stationId = ''
        value = 1000000
        iterator = it.newIterator(totalValues)
        while it.hasNext(iterator):
            info = it.next(iterator)
            if info['trips'] < value:
                value = info['trips']
                stationId = info['name']
        m.remove(citibike['totalStations'],stationId)
        lt.addLast(lst,stationId)

def changeInfo(citibike,lst,pos):
    """
    Intercambia el ID de la estación por su nombre correspondiente
    """
    lstCitibike = citibike['stations']
    iterator = it.newIterator(lstCitibike)
    stationId = lt.getElement(lst,pos)
    while it.hasNext(iterator):
            info = it.next(iterator)
            startStation = info['start station id']
            endStation = info['end station id']
            if stationId == startStation:
                stationId = info['start station name']
                lt.changeInfo(lst,pos,stationId)
                break
            elif stationId == endStation:           
                stationId = info['end station name']
                lt.changeInfo(lst,pos,stationId)
                break
###############################################

########## Requerimiento 5 ##########
def routeRecomendations(citibike,ageRange):
    """
    Informa la estación desde la cual las personas en el rango ingresado inician más viajes. 
    La estación donde terminan más viajes personas en rango y el camino mas corto en tiempo entre dicho par de estaciones.
    """     
    lstExit = lt.newList("ARRAY_LIST",compareValues)
    lstArrive = lt.newList("ARRAY_LIST",compareValues)
    findStationsInRange(citibike,ageRange,lstExit,lstArrive)  #Se guardan los ID de las estaciones dentro del rango
    if lt.size(lstExit) == 0 or lt.size(lstArrive) == 0:  #Si no se encuentran estaciones se para la función
        return -1
    data = {'exitStations': None,   #Total de viajes por estación
            'arriveStations':None}
    data['exitStations']=m.newMap(1019,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=compareStations)
    data['arriveStations']=m.newMap(1019,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=compareStations)
    itExit = it.newIterator(lstExit)
    itArrive = it.newIterator(lstArrive)
    while it.hasNext(itExit):
        id = it.next(itExit)
        addStartStation(data,id)
    while it.hasNext(itArrive):
        id = it.next(itArrive)
        addArriveStation(data,id)
    
    lstFinalExit = lt.newList("ARRAY_LIST")  #Listas para obtener las estaciones más usadas en el rango
    lstFinalArrive = lt.newList("ARRAY_LIST")
    obtainValues(data,lstFinalExit,'e')
    obtainValues(data,lstFinalArrive,'a')

    initStation = lt.getElement(lstFinalExit,1) #Estación inicial de la ruta (ID)
    finalStation = lt.getElement(lstFinalArrive,1) #Estación final de la ruta (ID)

    minimumCostPaths(citibike,initStation)
    path = minimumCostPath(citibike,finalStation) #Se calcula el camino de menor tiempo entre las dos estaciones

    lstPath = lt.newList("ARRAY_LIST",compareValues)
    if path is not None:   #Se agrega a una lista para poder asignar sus nombres respectivos
        while (not stack.isEmpty(path)):
            stop = stack.pop(path)
            if lt.isPresent(lstPath,stop['vertexA']) == 0:
                lt.addLast(lstPath,stop['vertexA'])
            if lt.isPresent(lstPath,stop['vertexB']) == 0:
                lt.addLast(lstPath,stop['vertexB'])
    else:
        pass
    changeInfo(citibike,lstFinalExit,1) #Se intercambia el ID por el nombre correspondiente de la estación
    changeInfo(citibike,lstFinalArrive,1)
    
    initStation = lt.getElement(lstFinalExit,1) #Estación inicial de la ruta (Nombre)
    finalStation = lt.getElement(lstFinalArrive,1) #Estación final de la ruta (Nombre)

    pos = 1
    while pos < lt.size(lstPath)+1:  #Se intercambia el ID por el nombre correspondiente de las estaciones en la ruta
        changeInfo(citibike,lstPath,pos)
        pos+=1

    lstReturn = lt.newList("ARRAY_LIST")
    
    lt.addLast(lstReturn,initStation)
    lt.addLast(lstReturn,finalStation)
    lt.addLast(lstReturn,lstPath)
    return lstReturn

#Funciones Helper
def findStationsInRange(citibike,ageRange,lst1,lst2):
    """
    Añade a las listas pasadas por parámetro las estaciones que se encuentren dentro del rango ingresado
    """
    
    iterator = it.newIterator(citibike['stations'])  #Lugar donde se encuentra la información de todas las estaicones
    while it.hasNext(iterator):
        info = it.next(iterator)
        ocurredDate = info['starttime']
        year=int(ocurredDate[:4])
        birthYear = int(info['birth year'])
        if ageRange[0] == "0":
            initRange = int(ageRange[0])
            finalRange = int(ageRange[2]+ageRange[3])
        elif ageRange == "60+" or ageRange=="60 +":
            initRange = 60
            finalRange = 120
        else: 
            initRange = int(ageRange[0]+ageRange[1])
            finalRange = int(ageRange[3]+ageRange[4])
        if (year - birthYear) >= initRange and (year - birthYear) <= finalRange:
            start = info['start station id']
            end = info['end station id']
            lt.addLast(lst1,start)  #Se añade a la lista de salidas
            lt.addLast(lst2,end) #Se añade a la lista de llegadas


def minimumCostPaths(citibike,station):
    """
    Calcula los caminos de costo mínimo desde la estación
    a todos los demas vertices del grafo
    """
    citibike['paths'] = djk.Dijkstra(citibike['graph'],station)
    return citibike

def minimumCostPath(citibike,station):
    """
    Retorna el camino de costo mínimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(citibike['paths'],station)
    return path
########################################

def touristRoute(citibike,lat1,lon1,lat2,lon2):
    near=findStations(citibike,lat1,lon1,lat2,lon2)
    path=djk.hasPathTo(near[0],near[1])


    return path

def findStations(citibike,lat1,lon1,lat2,lon2):
    iterator = it.newIterator(citibike['stations'])  #Lugar donde se encuentra la información de todas las estaicones
    while it.hasNext(iterator):
        info = it.next(iterator)
        lat_s=info['start station latitude']
        lon_s=info['start station longitude']
        short_st_distance=2000
        short_fn_distance=2000
        start_name=''
        finish_name=''
        startPoint=distance(lat1,lat_s,lon1,lon_s)
        finishPoint=distance(lat2,lat_s,lon2,lon_s)
        if startPoint < short_st_distance:
            short_st_distance=startPoint
            start_name=info['start station id']
        if finishPoint < short_fn_distance:
            short_fn_distance=finishPoint
            finish_name=info['start station id']
    return [start_name, finish_name]


#funcion helper Harvesine
from math import radians
from math import cos
from math import sin
from math import asin
from math import sqrt 
def distance(lat1, lat2, lon1, lon2): 
      
    # The math module contains a function named 
    # radians which converts from degrees to radians. 
    lon1 = radians(lon1) 
    lon2 = radians(lon2) 
    lat1 = radians(lat1) 
    lat2 = radians(lat2) 
       
    # Haversine formula  
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  
    c = 2 * asin(sqrt(a))  
     
    # Radius of earth in kilometers. Use 3956 for miles 
    r = 6371
       
    # calculate the result 
    return(c * r) 






#Funciones de comparación

def compareStations(station, keyvaluestation):
    """
    Compara dos estaciones
    """
    stationId = keyvaluestation['key']
    if (station == stationId):
        return 0
    elif (station > stationId):
        return 1
    else:
        return -1

def compareValues(v1,v2):
    if v1 == v2:
        return 0
    elif v1 > v2:
        return 1
    else:
        return -1

def compareValuesD(v1,v):
    v2 = v['key']
    if v1 == v2:
        return 0
    elif v1 > v2:
        return 1
    else:
        return -1