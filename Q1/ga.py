from ypstruct import struct
import numpy as np
import bisect # for fast sorting lists
import copy

def copy_edges_arr(edges_arr):
    edges_tmp = [edge.deepcopy() for edge in edges_arr]
    return edges_tmp

def calculate_edges_bit_arr(edges_arr):
    bit_arr = [None] * len(edges_arr)
    for i in range(len(bit_arr)):
        bit_arr[i] = 0 if edges_arr[i].deleted else 1
    print("BitArr:", bit_arr)
    for i in range(len(bit_arr)):
        print("i:", edges_arr[i].deleted)
    return bit_arr
        

def delete_edge(chromosome, index):
    chromosome.edges[index].deleted = True

def single_point_crossover(A, B, x):
    A_temp = np.array(A)
    B_temp = np.array(B)
    A_new = np.append(A_temp[:x], B_temp[x:]).toList()
    B_new = np.append(B_temp[:x], A_temp[x:]).toList()
    return A_new, B_new

# X denotes an array of crossover points
def multi_point_crossover(A, B, X):
    for i in X:
        A, B = single_point_crossover(A, B, i)
    return A, B

def uniform_crossover(A, B, P):
    for i in range(len(P)):
        if P[i] < 0.5:
            temp = A[i]
            A[i] = B[i]
            B[i] = temp
    return A, B



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
    npop = params.npop # population number
    maxit = params.maxit # maximum number of iterations
    pc = params.pc
    # nc is the number of children, which is pc times the number of parents
    # first divided by 2 and rounded, then multiplied by 2 to ensure that nc is an even number
    nc = np.round(pc*nc/2)*2 
    npoints = params.npoints


    # empty chromosome
    empty_chromosome = struct()
    empty_chromosome.cost = None
    empty_chromosome.edges = None
    empty_chromosome.edges_bit_arr = None

    # best solution
    best_chromosome = empty_chromosome.deepcopy()
    best_chromosome.cost = np.inf

    # worst solution
    worst_chromosome = empty_chromosome.deepcopy()
    worst_chromosome.cost = -np.inf

    # average solution
    avg_chromosome = empty_chromosome.deepcopy()
    avg_chromosome.cost = 0

    # ---------------------- INITIALIZING POPULATIONS ---------------------- #
    pop = empty_chromosome.repeat(npop) # returning an array of empty_chromosome of size npop
    for i in range(npop):
        pop[i].edges = copy_edges_arr(edges)
        # randomly delete edges
        random_positions = np.random.uniform(0, len(edges) - 1, nvar)
        for rand in random_positions:
            delete_edge(pop[i], int(round(rand)))
        pop[i].cost = cost(pop[i].edges)
        pop[i].edges_bit_arr = calculate_edges_bit_arr(pop[i].edges)

        if pop[i].cost < best_chromosome.cost:
            best_chromosome.edges = copy_edges_arr(pop[i].edges)
            best_chromosome.cost = pop[i].cost
            best_chromosome.edges_bit_arr = [i for i in pop[i].edges_bit_arr]
            print(best_chromosome.edges_bit_arr)

        if pop[i].cost > worst_chromosome.cost:
           worst_chromosome.cost = pop[i].cost
           worst_chromosome.edges_bit_arr = [i for i in pop[i].edges_bit_arr]

    print("Initial Population:")
    avg_chromosome.cost = sum(p.cost for p in pop)/npop
    print("{identity:<7} Chromosome: fitness = {fitness:.8f}, cost = {cost:.3f}".format(identity="Best", fitness=1/best_chromosome.cost, cost=best_chromosome.cost))
    print("{identity:<7} Chromosome: fitness = {fitness:.8f}, cost = {cost:.3f}".format(identity="Worst", fitness=1/worst_chromosome.cost, cost=worst_chromosome.cost))
    print("{identity:<7} Chromosome: fitness = {fitness:.8f}, cost = {cost:.3f}".format(identity="Average", fitness=1/avg_chromosome.cost, cost=avg_chromosome.cost))
    calculate_edges_bit_arr(best_chromosome.edges)

    # best cost of iterations
    bestcost = np.empty(maxit)

    # ---------------------- INITIALIZATION FINISHED ---------------------- #

    # Main loop
    for it in range(maxit):
        
        popc = [] # population of children
        
        # crossover loop
        for k in range(nc//2): # half of nc times (integer division)
            
            # select parents
            q = np.random.permutation(npop) # a random permutation from integers 0 to npop - 1
            p1 = pop[q[0]]
            p2 = pop[q[1]]

            # perform crossover
            c1 = empty_chromosome.deepcopy()
            c2 = empty_chromosome.deepcopy()
            p = np.random.rand(len(p1.edges_bit_arr))
            c1.edges_bit_arr, c2.edges_bit_arr = uniform_crossover(p1.edges_bit_arr, p2.edges_bit_arr, p)

            # perform mutation



        