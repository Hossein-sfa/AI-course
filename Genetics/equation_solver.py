from math import sin, cos, log10
from random import random, randint, choice
from time import time


# Equations
def equation1(a, x, y, z):
    return (a * x) + (y * (x ** 2)) + (y ** 3) + (z ** 3)


def equation2(b, x, y, z):
    return (b * y) + sin(y) + (2 ** y) - z + log10(abs(x) + 1)


def equation3(t, x, y, z):
    return (t * z) + y - (cos(x + y) / (sin((z * y) - (y ** 2) + z) + 2))


# Generation random person in format(x, y, z)
def random_person():
    return randint(-10, 10), randint(-10, 10), randint(-10, 10)


# Calculation fitness score of a person
def fitness(a, b, c, x, y, z):
    return equation1(a, x, y, z) ** 2 + equation2(b, x, y, z) ** 2 + equation3(c, x, y, z) ** 2


# Birth of a parson that is mean of parents
def birth(mother, father):
    return (mother[0] + father[0]) / 2, (mother[1] + father[1]) / 2, (mother[2] + father[2]) / 2


# find best person in population
def find_best_person(a, b, c, population):
    min = population[0]
    for person in population:
        if fitness(a, b, c, *person) < fitness(a, b, c, *min):
            min = person
    return min
     

# Genetics with 10% mutation with 1000 base population within 4.5 seconds with 0.000000000001 precision
def solver(a, b, c):
    population = [random_person() for _ in range(1000)]
    scores = {person: fitness(a, b, c, *person) for person in population}
    mutation = 0.1
    best_person = 0, 0, 0
    start = time()
    while time() - start < 4.5:
        if (time() - start) % 2 == 0:
            population = [random_person() for _ in range(5000)]
        new_population = []
        for _ in range(1000):
            tournament1 = [choice(population) for _ in range(10)]
            tournament2 = [choice(population) for _ in range(10)]
            mother = find_best_person(a, b, c, tournament1)
            father = find_best_person(a, b, c, tournament2)
            new_population.extend((birth(father, mother), father, mother))
        population = new_population
        if random() < mutation:
            population.append(random_person())
        scores = {person: fitness(a, b, c, *person) for person in population}
        current_best_person = min(scores, key=scores.get)
        if fitness(a, b, c, *current_best_person) < fitness(a, b, c, *best_person):
            best_person = current_best_person
        if fitness(a, b, c, *best_person) < 0.000000000001:
            return current_best_person
    return best_person
