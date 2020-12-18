from ypstruct import struct
import numpy as np
import bisect # for fast sorting lists
import copy

def delete_edge(chromosome, index):
    v1 = chromosome.edges[index].v1
    v2 = chromosome.edges[index].v2
    chromosome.edges[index].valid = False
    chromosome.graph[v1][v2] = 0
    chromosome.graph[v2][v1] = 0
    chromosome.deleted_edges = []
    bisect.insort(chromosome.deleted_edges, index)

def run(problem, params):
    
    # problem
    cost = problem.cost
    graph = problem.graph
    nvar = problem.nvar # number of variables
    steiner_vert = problem.steiner_vert
    terminal_vert = problem.terminal_vert
    vertices = problem.vertices
    edges = problem.edges 


    # parameters
    npop = params.npop = 5 # population number
    maxit = params.maxit = 100 # maximum number of iterations


    # empty chromosome
    empty_chromosome = struct()
    empty_chromosome.graph = None
    empty_chromosome.cost = None
    empty_chromosome.edges = None
    empty_chromosome.deleted_edges = None

    # best solution
    best_chromosome = empty_chromosome.deepcopy()
    best_chromosome.cost = np.inf

    # worst solution
    worst_chromosome = empty_chromosome.deepcopy()
    worst_chromosome.cost = - np.inf

    # average solution
    avg_chromosome = empty_chromosome.deepcopy()
    avg_chromosome.cost = 0

    # initializing population
    print(edges)
    pop = empty_chromosome.repeat(npop) # returning an array of empty_chromosome of size npop
    for i in range(npop):
        pop[i].graph = graph
        pop[i].edges = edges
        pop[i].cost = cost(pop[i].graph)[0]
        # randomly delete edges
        random_positions = np.random.uniform(0, len(edges) - 1, nvar)
        for rand in random_positions:
            delete_edge(pop[i], int(round(rand)))
        print(edges)

        # ....

        #if pop[i].cost < best_chromosome.cost:
        #    best_chromosome = pop[i].deepcopy()

        #if pop[i].cost > worst_chromosome.cost:
        #    worst_chromosome = pop[i].deepcopy()
        