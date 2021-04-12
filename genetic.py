import random
import math

'''
Laboratorio de Algoritmos genéticos:

Este archivo contiene las funciones que debe implementar para 
la práctica de laboratorio.

Ejercicio 1: operador de selección. Implementar la función selectRanking()
Ejercicio 2: operador de crossover. Implementar la función orderOneCrossover()
Ejercicio 3: operador de mutación. Implementar las funciones insertMutation() y swapMutation()

Instrucciones:
Este laboratorio cuenta con 2 archivos de código fuente de python:
    1. tsp.py: Programa principal que implementa la interfaz grafica y los parámetros para la ejecución
                del algoritmo genético a implementar. Leer este archivo para referencia del funcionamiento 
                general de la aplicación. En especial, revisar los métodos initHandler(), trainHandler() y nextHandler()
    2. genetic.py: Archivo con las funciones referentes a la implementación del algoritmo genético basado en permutaciones.
                En este archivo se implementa toda la funcionalidad referente al proceso de evolución de la población.

Para probar la aplicación o sus soluciones puede ejecutar el programa principal tsp.py usando: python tsp.py

'''

def initPopulation(cities, pop_size):
    '''
    Create a random list of candidate solutions.
    
    Return a list of candidates where each candidate is 
    a list of numbers corresponding to city ids.
    '''
    cities_id = [i for i in range(len(cities))]
    population = []
    for i in range(pop_size):
        candidate = cities_id.copy()
        random.shuffle(candidate)
        population.append(candidate)

    return population

def citiesDist(c1, c2, cities):
    '''
    Euclidian distance between 2 cities
    '''
    pos_c1 = cities[c1]['position']
    pos_c2 = cities[c2]['position']
    
    return math.sqrt((pos_c2[0] - pos_c1[0])**2 + (pos_c2[1] - pos_c1[1])**2)

def fitness(candidate, cities):
    '''
    returns the inverse of the travel cost for the given candidate
    '''
    total_dist = 0
    for i in range(len(candidate) - 1):
        total_dist += citiesDist(candidate[i], candidate[i + 1], cities)

    return total_dist

def getBest(population, cities, fitness=fitness):
    best = max(population, key=lambda c: fitness(c, cities))
    return fitness(best, cities), best 

def getWorst(population, cities, fitness=fitness):
    worst = min(population, key=lambda c: fitness(c, cities))
    return fitness(worst, cities), worst

def selectRoulette(population, cities):
    '''
    ----> Ejercicio 1 <----
    Implementar el operador de selección por el método de la RULETA.
    
    Usted debe modificar esta función para realizar la operación 
    de selección de las soluciones más competentes por el método de la ruleta.

    Esta función recibe 2 valores:
      population: es una lista de listas con permutaciones del orden de las ciudades a visitar.
                    por ejemplo, para un problema con 3 ciudades y una poblacion de 2 soluciones:
                        population = [[0,2,1], [2,1,0]]
      cities: es una lista de datos para cada ciudad. cada elemento es un diccionario {'position':(x, y), 'id':<id del punto en el GUI>}
    
    Esta función debe retornar una lista con el mismo número de candidatos que la lista population

    Tips:
        - para calcular el fitness de una solucion use lo siguiente: valor = fitness(candidato, cities), el candidato es un elemento
        de la lista population y cities es el mismo objeto que se recibe como parametro.
        - obtenga una nueva lista ordenada en forma descendente donde el primer elemento es el candidato más fuerte 
        o con valor de fitness mayor, y el último es el candidato más debil.
    '''
    fitness_list = []
    rulete = []
    new_generation = []
    number_population = len(population) 

    for solution in population: 
        fitness_list.append(fitness(solution,cities))
    fitness_total = sum(fitness_list)

    for i in range(number_population):
        percentage_i = fitness_list[i]/fitness_total
        ec_i = percentage_i * number_population
        ac_i = round(ec_i)
        dic = {'id':i,'solution': population[i],'ac':ac_i} 
        ''' Descomentar para probar
        if(i == 3):
            dic = {'id':i,'solution': population[i],'ac':2}
        if(i == 0):
            dic = {'id':i,'solution': population[i],'ac':0} 
        '''
        rulete.append(dic)
    rulete.sort(key=lambda p : p['ac'],reverse=True)
            
    for element in rulete:
        for i in range(element['ac']):
            new_generation.append(element['solution'])
    ''' Descomentar para probar
    print("======================================")
    print(rulete)
    print("======================================")
    print("======================================")
    print(new_generation)
    print("======================================")
    print(population)
    '''
    return new_generation 

def orderOneCrossover(parent1, parent2):
    '''
    ----> Ejercicio 2 <----
    Implementar el operador de crossover de orden 1.

    Usted debe modificar esta función para realizar la operación de crossover de 2 candidatos padres.
    
    Esta función recibe 2 valores:
        parent1: candidato 1, una lista con una permutación de ids de ciudades, por ejemplo, 
                para un problema con 4 ciudades, un candidato podría ser: [3,1,0,2]
        parent2: otro candidato
            v     v
        [2, 4, 1, 0, 3] [0, 3, 2, 4, 1] => [ 2, 4, 1, 0, 3]

    Esta función debe retornar un nuevo candidato hijo producto del crossover de los padres.

    Procedimiento:
    Para implementar correctamente la operación de crossover de orden 1 se recomienda seguir los siguientes pasos:
        1. crear una lista vacia del mismo tamaño que cualquier padre.
        2. obtener los puntos de inicio y final aleatorios para el segmento a copiar del padre 1.
        3. insertar el segmento del padre 1 en la misma posición en el hijo.
        4. completar los elementos restantes, en orden, del padre 2.
        5. retornar la solución hijo.
    
    Tips:
        - use funciones del módulo random para obtener números aleatorios.
        - use slicing de listas para insertar correctamente.
    '''
    from random import random
    p_size = len(parent1)
    # crear lista de elementos vacios
    child = [None] * p_size

    point_s = int(random()*p_size)
    point_f = int(random()*p_size+1)

    if(point_s>=point_f): 
        aux = point_f
        point_f = point_s
        point_s = aux

    child[point_s:point_f] = parent1[point_s:point_f] 
    i = point_f%p_size
    j = i+1
    aux = j
    complete = False
    while i<p_size and not(complete):
        j=aux%p_size
        while j<p_size and not(complete):
            if(len([item for item in child if item in parent2])==p_size):
                complete = True
            if(not(parent2[j] in child)):
                child[i] = parent2[j] 
                aux = i
                j = p_size
            else:
                if(not(complete)):
                    j=(j+1)%p_size
        i = (i+1)%p_size

    return child

def nextOffspring(population, crossover=orderOneCrossover, elitism=0.0):
    '''
    Generate a new offspring based on given populations. Generate a list of parents 
    to crossover and get 2 childs for each pair.
    Assumes population is ordered.

    returns a new population corresponding to the offspring
    '''
    n_elite = int(len(population) * elitism)

    # print(f'elite: {n_elite}')
    elite_candidates = []
    new_population = []
    if n_elite == 0:
        new_population = population
    else:
        elite_candidates = population[:n_elite]
        new_population = population[:-n_elite]

    # print(f'total pop: {len(elite_candidates)} + {len(new_population)}')
    # make pairs
    
    parents = [(new_population[i], new_population[i + 1]) for i in range(len(new_population) // 2)]
    
    offspring = []
    for parent1, parent2 in parents:
        # get first child
        child1 = crossover(parent1, parent2)
        offspring.append(child1)

        # repeat second child 
        child2 = crossover(parent2, parent1)
        offspring.append(child2)

    # odd number of parents, crossover the last 2 ones once
    if len(new_population) % 2:
        parent1 = new_population[-1]
        parent2 = new_population[-2]
        
        child1 = crossover(parent1, parent2)
        offspring.append(child1)

    return elite_candidates + offspring

def insertMutation(candidate):
    new_candidate = candidate
    print("=================")
    print(new_candidate)
    return new_candidate

def swapMutation(candidate):
    from random import random
    p_size = len(candidate)
    equals = True
    new_candidate = [None] * p_size
    while equals:
        point_1 = int(random() * p_size)
        point_2 = int(random() * p_size)
        equals = False
        if(point_1 == point_2):
            point_1 = int(random() * p_size)
            point_2 = int(random() * p_size)
            equals = True

    if(point_1>=point_2): 
            aux = point_2
            point_2 = point_1
            point_1 = aux
    new_candidate = candidate.copy()
    aux_list = candidate[point_1+1:point_2]
    new_candidate[point_1+1] = candidate[point_2]
    new_candidate[point_1+2:point_2+1] = aux_list

    return new_candidate

def mutate(population, mutation=swapMutation, prob=0.10):
    new_population = []
    for c in population:
        if random.random() < prob:
            new_population.append(mutation(c))
        else:
            new_population.append(c)

    return new_population

