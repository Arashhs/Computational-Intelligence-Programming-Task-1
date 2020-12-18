from ypstruct import structure
import numpy as np
import bisect # for fast sorting lists
import copy

def copy_edges_arr(edges_arr):
    edges_tmp = [edge.deepcopy() for edge in edges_arr]
    return edges_tmp

def bit_arr_to_edges(edges_bit_arr, edges_arr):
    edges_res = copy_edges_arr(edges_arr)
    for i in range(len(edges_arr)):
        edges_res[i].deleted = True if edges_bit_arr[i] == 0 else False
    return edges_res

def edges_to_bit_arr(edges_arr):
    bit_arr = [None] * len(edges_arr)
    for i in range(len(bit_arr)):
        bit_arr[i] = 0 if edges_arr[i].deleted else 1
    return bit_arr
        

def delete_edge(chromosome, index):
    chromosome.edges[index].deleted = True

def single_point_crossover(A, B, x):
    A_temp = np.array(A)
    B_temp = np.array(B)
    A_new = np.append(A_temp[:x], B_temp[x:]).tolist()
    B_new = np.append(B_temp[:x], A_temp[x:]).tolist()
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

# mu is the probability of mutation for each bit
def mutation(A, mu):
    res = [i for i in A]
    flag = np.random.rand(len(A)) <= mu
    for i in range(len(flag)):
        if flag[i]:
            res[i] = 1 if A[i] == 0 else 0
    return res

def roulette_wheel_selection(p):
    c = np.cumsum(p)
    r = sum(p) * np.random.rand()
    ind = np.argwhere(r <= c)
    return ind[0][0]




def run(problem, params):
    
    # problem
    cost = problem.cost
    graph = problem.graph
    nvar = problem.nvar # number of variables
    steiner_vert = problem.steiner_vert
    terminal_vert = problem.terminal_vert
    vertices = problem.vertices
    edges = problem.edges 
    plot_graph = problem.plot_graph
    build_graph = problem.build_graph
    calculate_cost4 = problem.calculate_cost4


    # parameters
    npop = params.npop # population number
    maxit = params.maxit # maximum number of iterations
    pc = params.pc
    # nc is the number of children, which is pc times the number of parents
    # first divided by 2 and rounded, then multiplied by 2 to ensure that nc is an even number
    nc = int(np.round(pc*npop/2)*2) 
    npoints = params.npoints
    mu = params.mu
    beta = params.beta


    # empty chromosome
    empty_chromosome = structure()
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
        pop[i].edges_bit_arr = edges_to_bit_arr(pop[i].edges)

        if pop[i].cost < best_chromosome.cost:
            best_chromosome.edges = copy_edges_arr(pop[i].edges)
            best_chromosome.cost = pop[i].cost
            best_chromosome.edges_bit_arr = [i for i in pop[i].edges_bit_arr]

        if pop[i].cost > worst_chromosome.cost:
            worst_chromosome.edges = copy_edges_arr(pop[i].edges)
            worst_chromosome.cost = pop[i].cost
            worst_chromosome.edges_bit_arr = [i for i in pop[i].edges_bit_arr]

    print("Initial Population:")
    avg_chromosome.cost = sum(p.cost for p in pop)/npop
    print("{identity:<7} Chromosome: fitness = {fitness:.8f}, cost = {cost:.3f}".format(identity="Best", fitness=1/best_chromosome.cost, cost=best_chromosome.cost))
    print("{identity:<7} Chromosome: fitness = {fitness:.8f}, cost = {cost:.3f}".format(identity="Worst", fitness=1/worst_chromosome.cost, cost=worst_chromosome.cost))
    print("{identity:<7} Chromosome: fitness = {fitness:.8f}, cost = {cost:.3f}".format(identity="Average", fitness=1/avg_chromosome.cost, cost=avg_chromosome.cost))
    print("\n")

    # best cost of iterations
    bestcost = np.empty(maxit)

    # ---------------------- INITIALIZATION FINISHED ---------------------- #

    # Main loop
    for it in range(maxit):

        costs = np.array([p.cost for p in pop])
        avg_cost = np.mean(costs)
        if avg_cost != 0:
            costs = costs/avg_cost # normalization
        probs = np.exp(-beta*costs)
        
        popc = [] # population of children
        
        # crossover loop
        for k in range(nc//2): # half of nc times (integer division)
            
            # select parents
            # q = np.random.permutation(npop) # a random permutation from integers 0 to npop - 1
            # p1 = pop[q[0]]
            # p2 = pop[q[1]]

            # perform RW (Roulette Wheel) selection
            p1 = pop[roulette_wheel_selection(probs)]
            p2 = pop[roulette_wheel_selection(probs)]

            # perform crossover
            c1 = empty_chromosome.deepcopy()
            c2 = empty_chromosome.deepcopy()
            p = np.random.rand(len(p1.edges_bit_arr))
            c1.edges_bit_arr, c2.edges_bit_arr = uniform_crossover(p1.edges_bit_arr, p2.edges_bit_arr, p)
            # p = np.random.randint(len(edges), size=npoints)
            # c1.edges_bit_arr, c2.edges_bit_arr = multi_point_crossover(p1.edges_bit_arr, p2.edges_bit_arr, p)


            c1.edges = bit_arr_to_edges(c1.edges_bit_arr, edges)
            c2.edges = bit_arr_to_edges(c2.edges_bit_arr, edges)

            
            # perform mutation
            c1.edges_bit_arr = mutation(c1.edges_bit_arr, mu)
            c2.edges_bit_arr = mutation(c2.edges_bit_arr, mu)

            # update c1 and c2 edges
            c1.edges = bit_arr_to_edges(c1.edges_bit_arr, c1.edges)
            c1.edges = bit_arr_to_edges(c2.edges_bit_arr, c2.edges)

            # evaluate first offspring
            c1.cost = cost(c1.edges)
            if c1.cost < best_chromosome.cost:
                best_chromosome.edges = copy_edges_arr(c1.edges)
                best_chromosome.cost = c1.cost
                best_chromosome.edges_bit_arr = [i for i in c1.edges_bit_arr]

            if c1.cost > worst_chromosome.cost:
                worst_chromosome.edges = copy_edges_arr(c1.edges)
                worst_chromosome.cost = c1.cost
                worst_chromosome.edges_bit_arr = [i for i in c1.edges_bit_arr]

            # evaluate second offspring
            c2.cost = cost(c2.edges)
            if c2.cost < best_chromosome.cost:
                best_chromosome.edges = copy_edges_arr(c2.edges)
                best_chromosome.cost = c2.cost
                best_chromosome.edges_bit_arr = [i for i in c2.edges_bit_arr]

            if c1.cost > worst_chromosome.cost:
                worst_chromosome.edges = copy_edges_arr(c2.edges)
                worst_chromosome.cost = c2.cost
                worst_chromosome.edges_bit_arr = [i for i in c2.edges_bit_arr]

            # add offsprings to popc
            popc.append(c1)
            popc.append(c2)

        # merge, sort, and select
        pop += popc # Lambda + mu selection
        pop = sorted(pop, key=lambda p: p.cost)
        pop = pop[0:npop] # top npop population

        # store best cost
        bestcost[it] = best_chromosome.cost

        # print information
        avg_chromosome.cost = sum(p.cost for p in pop)/npop
        print("Iteration:", it)
        print("{identity:<7} Chromosome: fitness = {fitness:.8f}, cost = {cost:.3f}".format(identity="Best", fitness=1/best_chromosome.cost, cost=best_chromosome.cost))
        print("{identity:<7} Chromosome: fitness = {fitness:.8f}, cost = {cost:.3f}".format(identity="Worst", fitness=1/worst_chromosome.cost, cost=worst_chromosome.cost))
        print("{identity:<7} Chromosome: fitness = {fitness:.8f}, cost = {cost:.3f}".format(identity="Average", fitness=1/avg_chromosome.cost, cost=avg_chromosome.cost))
        print("\n")
    
    best_chromosome.cost = calculate_cost4(best_chromosome.edges)
    plot_graph(build_graph(best_chromosome.edges))
    print("Final Best Cost:", best_chromosome.cost)
        

    # output
    out = structure()
    out.pop = pop





        