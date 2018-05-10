# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 10:09:10 2017

@author: mjack
"""

import random

pistas = [
(3,[3,1,6,9,4,1,0,6,1,7,1,2,9,4,1,7]), 
(3,[6,4,5,7,9,6,5,7,6,8,7,0,1,2,6,8]),
(1,[8,9,6,1,6,8,5,7,6,1,4,5,8,0,6,1]),
(1,[7,5,3,8,9,2,5,3,1,8,3,4,3,8,7,0]), 
(1,[8,3,1,6,4,6,9,6,8,5,6,7,2,9,2,9]), 
(2,[4,7,3,2,4,2,0,1,6,6,8,9,7,9,5,5]), 
(3,[5,1,6,4,9,2,2,2,0,1,0,7,9,8,2,8]),
(2,[7,6,6,4,9,9,5,0,2,2,0,6,4,1,7,9]),
(3,[9,7,5,0,0,5,2,9,2,3,2,4,7,4,2,6]),
(3,[8,0,6,3,7,8,3,3,3,1,4,4,6,7,8,2]), 
(1,[6,9,5,2,1,4,4,7,2,4,3,5,0,8,0,7]),
(2,[4,8,4,7,2,0,5,6,1,3,4,1,3,6,6,9]), 
(1,[9,3,2,1,8,2,7,8,6,6,3,3,9,6,9,8]), 
(2,[6,2,3,8,2,2,5,0,5,6,3,6,7,3,3,1]),
(2,[4,7,2,5,9,7,4,7,8,1,8,3,7,9,7,1]),
(0,[4,8,4,3,8,9,7,3,0,6,8,0,8,9,6,2]), 
(3,[1,9,5,0,5,1,3,2,6,9,5,0,9,0,7,1]),
(3,[2,9,2,2,6,7,4,5,6,0,9,3,0,2,9,1]), 
(1,[7,8,1,2,1,3,3,5,3,2,0,1,1,0,2,0]),
(2,[2,7,3,7,3,9,2,7,2,0,2,3,9,4,5,8]),
(3,[3,9,6,3,4,8,7,6,2,6,8,4,6,2,9,5]), 
(2,[2,4,2,3,2,9,8,8,1,5,7,6,6,8,4,4]) ]








"""
FUNCIONES

"""

# --Generar poblacion

def generar_individuo():
    return [random.randint(0,9) for i in range (16)]

def generar_poblacion():
    return [generar_individuo() for i in range (1000)]


# --Fitness
def funcion_fitness(individuo):
    ac = 0
    peso = 1
    resultado = 0
    
    for pista in pistas:
        ac = 0
        for i in range(len(individuo)):
            if(pista[1][i] == individuo [i]):
                ac += 1
        peso = (ac-pista[0])**2
        resultado += peso 
    
    return resultado


def fitness_poblacion(poblacion):
    return [( funcion_fitness(i), i) for i in poblacion ]



# --CRUCE

def cruce_parcial(I1, I2):
    
    i = random.randint(0,15)
    j = random.randint(i+1,16)
    
    
    subI1 = I1.copy()[i:j]
    subI2 = I2.copy()[i:j]
    
    
    newI1 = I1[:]
    newI2 = I2[:]
    
    newI2[i:j] = subI1
    newI1[i:j]= subI2
         
    return (newI1, newI2)

def cruzar(individuos):
    return [ cruce_parcial(individuos[i*2], individuos[(i*2)+1]) for i in range (len(individuos)//2)]

# -- MUTAR

def mutacion_uniforme(individuo, prob_m):
    for i in range(len(individuo)):
        if random.random()<=prob_m:
            nuevo_valor=random.randint(0,9)
            individuo[i]=nuevo_valor
    return individuo 

def mutar_hijos(hijos, prob_m):
    return [mutacion_uniforme(j, prob_m) for i in hijos for j in i]

# --SELECCION

def selecciontorneo(poblacion,k,tamaño):
    seleccionados=[]
    for i in range(tamaño):
        individuostorneo = []
        for n in range(k):
            individuostorneo.append(random.choice(poblacion))
        individuostorneo.sort()
        seleccionados.append(individuostorneo[0][1])
    return seleccionados

# --REEMPLAZAMIENTO

def reemplazamiento_aleatorio(poblacion, nuevos_individuos):
   
    poblacion_sorted = [i[1] for i in sorted (poblacion, reverse=True)]   
    for i in range(len(nuevos_individuos)):
        if random.random() >= ( 1/len(poblacion)):
            poblacion_sorted[i] = nuevos_individuos[i]
        else:
            poblacion_sorted[ random.randint(0, len(poblacion_sorted)-1) ] = nuevos_individuos[i]
        
    
    return poblacion_sorted
        


def busqueda_localizada(fenotipo):
    
    centro = fenotipo[1][:]
    vecinos = []
    vecinos.append(fenotipo)
    
    for i in range(16):
        for num in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            centro[i] = num
            vecinos.append( (funcion_fitness(centro), centro) )
            centro[i] = fenotipo[1][i]
    
    vecinos.sort()
    return vecinos
        

"""

*********** ALGORITMO ***********

"""




parada = 50000
iteracion = 0
 
poblacion = generar_poblacion()
poblacion = fitness_poblacion(poblacion)
poblacion.sort(reverse=True)

print("\nSemilla inicial: ", poblacion)
print("\nEspere...") 

while(iteracion < parada):
     
   seleccionados = selecciontorneo(poblacion, 3, 200)
    
    
   hijos = cruzar(seleccionados)
   nuevos_individuos = mutar_hijos(hijos, 0.3)
    
    
   poblacion = reemplazamiento_aleatorio(poblacion, nuevos_individuos)
   poblacion = fitness_poblacion(poblacion)
    
   iteracion +=1
 
 
poblacion.sort(reverse=True)

ref = poblacion[ len(poblacion)-1 ][0]

print("\nResultado: ",poblacion)
print("\nMejor candidato ", poblacion[(len(poblacion)-1)]   )

print("\nBusqueda del mejor vecino: ", busqueda_localizada(poblacion[(len(poblacion)-1)])[0])                 
                    