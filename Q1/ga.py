from ypstruct import struct
import numpy as np

def run(problem, params):
    
    # problem
    problem = struct()
    cost = problem.cost
    graph = problem.graph

    # parameters
    npop = params.npop = 5 # population number
    maxit = params.maxit = 100 # maximum number of iterations
    steiner_vert = params.steiner_vert
    terminal_vert = params.terminal_vert
    vertices = params.vertices 

    # empty chromosome
    empty_chromosome = struct()
    empty_chromosome.graph = None
    empty_chromosome.cost = None

    # best solution
    best_chromosome = empty_chromosome.deepcopy()
    best_chromosome.cost = np.inf

    # worst solution
    worst_chromosome = empty_chromosome.deepcopy()
    worst_chromosome.cost = np.inf

    # average solution
    avg_chromosome = empty_chromosome.deepcopy()
    avg_chromosome.cost = np.inf

    # initializing population
    pop = empty_chromosome.repeat(npop) # returnin an array of empty_chromosome of size npop
    for i in range(npop):
        # randomly delete edges

        # ....

        if pop[i].cost < best_chromosome.cost:
            best_chromosome = pop[i].deepcopy()

        if pop[i].cost > worst
        