# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 15:42:17 2017

@author: mjack

"""


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





import random



def generate_gen():
    first = str(random.randint(0,1))
    if first == '1':
        return first+'00'+str(random.randint(0,1))
    else:
        return first + str(random.randint(0,1)) + str(random.randint(0,1)) + str(random.randint(0,1))

def generate_genotipo():
    return [generate_gen() for i in range(16)]

def generate_population():
    return [generate_genotipo() for i in range (1000)]









def traslateToBin(numer):
    return bin(numer)[2:].zfill(4)

def traslateToGenotipo(genotipo):
    return genotipo[0], [ ( traslateToBin(i) ) for i in genotipo[1]  ]


def fitness(fenotipo):
    ac = 0
    peso = 1
    resultado = 0
    
    for i in pistas:
        
        genotipo = traslateToGenotipo(i)
        
        ac = 0
        for i in range(len(fenotipo)):
            if(genotipo[1][i] == fenotipo [i]):
                ac += 1
        peso = (ac-genotipo[0])**2
        resultado += peso 
    
    return resultado



def fitness_population(poblacion):
    return [( fitness(i), i) for i in poblacion ]


def tournament_selection(poblacion,k,tamaño):
    seleccionados=[]
    for i in range(tamaño):
        individuostorneo = []
        for n in range(k):
            individuostorneo.append(random.choice(poblacion))
        individuostorneo.sort()
        seleccionados.append(individuostorneo[0][1])
    return seleccionados

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

def mate(subPopulation):
    return [ cruce_parcial(subPopulation[i*2], subPopulation[(i*2)+1]) for i in range (len(subPopulation)//2)]

def mutacion_uniforme(individuo, prob_m):
    for i in range(len(individuo)):
        if random.random()<=prob_m:
            individuo[i]=generate_gen()
    return individuo

def mutate(hijos, prob_m):
    return [mutacion_uniforme(j, prob_m) for i in hijos for j in i]

def random_replacement(poblacion, nuevos_individuos):
   
    poblacion_sorted = [i[1] for i in sorted (poblacion, reverse=True)]   #ordeno a la poblacion por su fitness de peor a mejor, quedandome solo con el elemento
    for i in range(len(nuevos_individuos)):
        if random.random() >= ( 1/len(poblacion)):
            poblacion_sorted[i] = nuevos_individuos[i]
        else:
            poblacion_sorted[ random.randint(0, len(poblacion_sorted)-1) ] = nuevos_individuos[i]
        
    
    return poblacion_sorted

def traslateToDec(gen):
    return int(gen, 2)

def traslateToFenotipe(genotipe):
    return [traslateToDec(i) for i in genotipe]

def traslatePopulationFromGenotipesToFenotipes(population):
    return  [ (i[0], traslateToFenotipe(i[1])) for i in population ]




"""

*********** ALGORITMO ***********

"""


stop = 5000
start = 0

population = generate_population()
population = fitness_population(population)
population.sort(reverse=True)

print("\nSemilla inicial: ", population)

while(start < stop):

    

    selections = tournament_selection(population, 3, 200)
    sons = mate(selections)
    new_population = mutate(sons, 0.3)

    population = random_replacement(population, new_population)
    population = fitness_population(population)

    start +=1
    
population = traslatePopulationFromGenotipesToFenotipes(population)
population.sort(reverse=True)
print("\nPoblación resultante: ", population)
print("\nMejor candidato ", population[(len(population)-1)]   )







