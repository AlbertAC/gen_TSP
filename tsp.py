from tkinter import *
from tkinter.ttk import *
from time import sleep
import random
from random import randint
from genetic import *

import time

class TSPApp():
    SIZE = 3
    def __init__(self):
        self.cities = []
        self.lines = []
        self.c_labels = []
        self.root = Tk()
        self.root.title("Genetic TSP")
        self.root.geometry('800x520')

        self.map = Canvas(self.root, width=720, height=370)
        self.map.grid(column=0, row=0, columnspan=5)
        self.map.configure(bg='white')
        
        self.debug_lbl = Label(self.root, text='Mensaje:')
        self.debug_lbl.grid(column=0, row=1)

        self.debug_msg = Label(self.root, text='-')
        self.debug_msg.grid(column=0, row=1, columnspan=5)

        self.cities_lbl = Label(self.root, text='Numero de ciudades')
        self.cities_lbl.grid(column=0, row=2)

        self.cities_spin = Spinbox(self.root, from_=5, to=50, width=5)
        self.cities_spin.grid(column=1, row=2)

        self.generate_btn = Button(self.root, text='Generar  \nCiudades', command=self.generateHandler)
        self.generate_btn.grid(column=2, row=2)

        self.init_lbl = Label(self.root, text='Tamaño de la poblacion')
        self.init_lbl.grid(column=0, row=3)

        self.init_txt = Entry(self.root, width=4, state=DISABLED)
        self.init_txt.grid(column=1, row=3)

        self.init_btn = Button(self.root, text='Iniciar Poblacion', command=self.initHandler, state=DISABLED)
        self.init_btn.grid(column=2, row=3)

        self.train_btn = Button(self.root, text='Entrenar', command=self.trainHandler, state=DISABLED)
        self.train_btn.grid(column=4, row=3)

        self.train_steps_lbl = Label(self.root, text='Steps')
        self.train_steps_lbl.grid(column=5, row=2)

        self.train_steps_txt = Entry(self.root, width=5, state=DISABLED)
        self.train_steps_txt.grid(column=5, row=3)

        self.next_btn = Button(self.root, text='Siguiente Gen.', command=self.nextHandler, state=DISABLED)
        self.next_btn.grid(column=3, row=3)
        
        self.elitism_lbl = Label(self.root, text='Elitismo')
        self.elitism_lbl.grid(column=0, row=4)

        self.elitism_spin = Spinbox(self.root, from_=0, to=50, width=5)
        self.elitism_spin.grid(column=1, row=4)

        self.mut_rate_lbl = Label(self.root, text='Proporcion de \nmutacion')
        self.mut_rate_lbl.grid(column=0, row=5)

        self.mut_rate_spin = Spinbox(self.root, from_=0, to=100, width=5)
        self.mut_rate_spin.grid(column=1, row=5)

        self.population = []
        self.generation = 0
        self.best = (0, [])
        self.root.mainloop()

    def generateHandler(self):
        self.cleanSolution()
        self.cleanCities()
        self.cleanDebug()
        self.best = (0, [])
        n = int(self.cities_spin.get())
        w = int(self.map.config('width')[-1])
        h = int(self.map.config('height')[-1])
        print(f'Generando: {n} ciudades...')
        print(f'Map Size: ({w},{h})')
        for i in range(n):
            x = randint(0, w - self.SIZE)
            y = randint(0, h - self.SIZE)
            city = {'position': (x, y), 'id': self.map.create_rectangle(x, y, x + self.SIZE, y + self.SIZE, fill='red', tags=str(i))}
            self.c_labels.append(self.map.create_text(x - 3,y - 6,text=str(i)))
            self.cities.append(city)

        self.init_txt['state'] = NORMAL
        self.init_btn['state'] = NORMAL

    def drawSolution(self, candidate, color='blue'):
        self.cleanSolution()
        for i in range(len(candidate) - 1):
            l = self.map.create_line(self.cities[candidate[i]]['position'][0], 
                                    self.cities[candidate[i]]['position'][1],
                                    self.cities[candidate[i+1]]['position'][0],
                                    self.cities[candidate[i+1]]['position'][1], fill=color)
            self.lines.append(l)
        # return lines

    def initHandler(self):
        if self.init_txt.get() == '':
            self.error('debe especificar poblacion')
            return
        self.cleanDebug()
        self.cleanSolution()
        self.best = (0, [])
        try:
            pop_size = int(self.init_txt.get())
        except ValueError as e:
            self.error('tamaño inválido, debe ingresar un número entero')
            return

        first = initPopulation(self.cities, pop_size)
        self.population = first
        # draw a candidate
        best = getBest(first, self.cities)
        self.drawSolution(best[1])
        self.message(f'best: {best[0]}')
        print(f'best: {best}')
        self.next_btn['state'] = NORMAL
        self.train_btn['state'] = NORMAL
        self.train_steps_txt['state'] = NORMAL

    def trainHandler(self):
        n_steps = 0
        self.generation = 0
        if self.train_steps_txt.get() == '':
            self.error('debe especificar cantidad pasos')
            return
        self.cleanDebug()
        self.cleanSolution()
        try:
            n_steps = int(self.train_steps_txt.get())
        except ValueError as e:
            self.error('dato inválido, debe ingresar un número entero')
            return
        start_time = time.time()

        for i in range(n_steps):
            self.nextHandler()

        self.message(f'best of training{self.generation}: {self.best[0]}')
        print(f'execution time: {(time.time() - start_time)}')
        print(f'best of training{self.generation}: {self.best}')
        self.drawSolution(self.best[1])

    def nextHandler(self):
        elitism = int(self.elitism_spin.get()) / 100.0
        mut_rate = int(self.mut_rate_spin.get()) / 100.0
        
        parents = selectRoulette(self.population, self.cities)
        children = nextOffspring(parents, elitism=elitism)
        new = mutate(children, prob=mut_rate)
        best = getBest(new, self.cities)
        if best[0] > self.best[0]:
            self.best = best
            self.drawSolution(best[1])
            
        self.generation +=1
        print(best[0])
        self.population = new

    def cleanSolution(self):
        for l in self.lines:
            self.map.delete(l)
        self.lines = []

    def cleanCities(self):
        for c in self.cities:
            self.map.delete(c['id']) 
        self.cities = []

        for c in self.c_labels:
            self.map.delete(c) 
        self.c_labels = []

    def cleanDebug(self):
        self.debug_msg['text'] = '-'

    def error(self, error):
        self.debug_msg['text'] = f'ERROR: {error}'
    def message(self, msg):
        self.debug_msg['text'] = msg

if __name__ == '__main__':
    app = TSPApp()