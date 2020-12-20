from ypstruct import structure
import numpy as np
import math

def crossover(p1, p2, gamma=0.1):
    c1 = p1.deepcopy()
    c2 = p2.deepcopy()
    alpha = np.random.uniform(-gamma, 1+gamma, *c1.x.shape)
    c1.x = alpha*p1.x + (1-alpha)*p2.x
    c2.x = alpha*p2.x + (1-alpha)*p1.x
    return c1, c2


def run(problem, params):
    
    # problem
    eggholder_func = problem.eggholder_func
    fitness_func = problem.fitess_func
    nvar = problem.nvar
    varmin = problem.varmin
    varmax = problem.varmax 


    # parameters
    npop = params.npop # population number
    maxit = params.maxit # maximum number of iterations
    sigma = params.sigma # learning rate
    pc = params.pc # children population
    gamma = params.gamma
    # nc is the number of children, which is pc times the number of parents
    # first divided by 2 and rounded, then multiplied by 2 to ensure that nc is an even number
    nc = int(np.round(pc*npop/2)*2) 

    # empty chromosome
    empty_chromosome = structure()
    empty_chromosome.f = None # f = EggHolder(x)
    empty_chromosome.fitness = None
    empty_chromosome.x = None # x = [x1, x2]
    empty_chromosome.sigma = sigma # learning rate

    # best solution
    best_chromosome = empty_chromosome.deepcopy()
    best_chromosome.fitness = 0

    # worst solution
    worst_chromosome = empty_chromosome.deepcopy()
    worst_chromosome.fitness = np.inf

    # initalizing population
    pop = empty_chromosome.repeat(npop)
    for i in range(npop):
        pop[i].x = np.random.uniform(varmin, varmax, nvar)
        pop[i].f = eggholder_func(pop[i].x)
        pop[i].fitness = fitness_func(pop[i].f)

        if pop[i].fitness >= best_chromosome.fitness:
            best_chromosome = pop[i].deepcopy()
            
        if pop[i].fitness <= worst_chromosome.fitness:
            worst_chromosome = pop[i].deepcopy()

    print("Initial Population:")
    avg_fitness = sum(p.fitness for p in pop)/npop
    avg_f = sum(p.f for p in pop)/npop
    print("{identity:<7} Chromosome: fitness = {fitness:.8f}, f = {cost:.3f}".format(identity="Best", fitness=best_chromosome.fitness, cost=best_chromosome.f))
    print("{identity:<7} Chromosome: fitness = {fitness:.8f}, f = {cost:.3f}".format(identity="Worst", fitness=worst_chromosome.fitness, cost=worst_chromosome.f))
    print("{identity:<7} Chromosome: fitness = {fitness:.8f}, f = {cost:.3f}".format(identity="Average", fitness=avg_fitness, cost=avg_f))
    print("\n")

    # best cost of iterations
    bestcost = np.empty(maxit)

    # main loop
    for it in range(maxit):

        popc = []

        # mutation
        for j in range(len(popc)):
            popc[j].sigma = popc[j].sigma * math.exp(popc[j].sigma * np.random.randn())
            popc[j].x = popc[j].x + popc[j].sigma * np.random.randn(*popc[j].x.shape)


        # parent selection and crossover
        for k in range(nc//2):

            # select parents
            q = np.random.permutation(npop) # a random permutation from integers 0 to npop - 1
            p1 = pop[q[0]] # random first parent
            p2 = pop[q[1]] # random second parent

            # perform corssover
            c1, c2 = crossover(p1, p2)

            # evaluate first offspring
            c1.f = eggholder_func(c1.x)
            c1.fitness = fitness_func(c1.f)

            if c1.fitness >= best_chromosome.fitness:
                best_chromosome = c1.deepcopy()
            
            if c1.fitness <= worst_chromosome.fitness:
                worst_chromosome = c1.deepcopy()

            # evaluate second offspring
            c2.f = eggholder_func(c2.x)
            c2.fitness = fitness_func(c2.f)

            if c2.fitness >= best_chromosome.fitness:
                best_chromosome = c2.deepcopy()
            
            if c2.fitness <= worst_chromosome.fitness:
                worst_chromosome = c2.deepcopy()

            # add offsprings to popc
            popc.append(c1)
            popc.append(c2)

        # merge, sort, and select
        pop = popc # Lambda, mu selection
        pop = sorted(pop, key=lambda p: p.fitness, reverse=True)
        pop = pop[0:npop] # top npop population

        # store best cost
        bestcost[it] = best_chromosome.cost

        # print information
        avg_fitness = sum(p.fitness for p in pop)/npop
        avg_f = sum(p.f for p in pop)/npop
        print("Iteration:", it)
        print("{identity:<7} Chromosome: fitness = {fitness:.8f}, f = {cost:.3f}".format(identity="Best", fitness=best_chromosome.fitness, cost=best_chromosome.f))
        print("{identity:<7} Chromosome: fitness = {fitness:.8f}, f = {cost:.3f}".format(identity="Worst", fitness=worst_chromosome.fitness, cost=worst_chromosome.f))
        print("{identity:<7} Chromosome: fitness = {fitness:.8f}, f = {cost:.3f}".format(identity="Average", fitness=avg_fitness, cost=avg_f))
        print("\n")

    print("Final Result:\nResulted Global Minimum = {}, x1 = {}, x2 = {}".format(best_chromosome.f, best_chromosome.x[0], best_chromosome.x[1]))    



    # output
    out = structure()
    out.pop = pop
    return out