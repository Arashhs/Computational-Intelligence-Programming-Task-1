from ypstruct import structure
import numpy as np
import math




def schedule_day(nurses_num=8, max_shifts_num=9):
    shift1_num = np.random.randint(2, 4)
    sched1 = np.random.choice(range(1, (nurses_num + 1)), shift1_num, replace=False).tolist()
    while len(sched1) < 3:
        sched1.append(0)
    shift2_num = np.random.randint(2, 5)
    sched2 = np.random.choice(range(1, (nurses_num + 1)), shift2_num, replace=False).tolist()
    while len(sched2) < 4:
        sched2.append(0)
    shift3_num = np.random.randint(1, 3)
    sched3 = np.random.choice(range(1, (nurses_num + 1)), shift3_num, replace=False).tolist()
    while len(sched3) < 2:
        sched3.append(0)

    sched = sched1 + sched2 + sched3
    return sched


def schedule_week(nurses_num=8, max_shifts_num=9):
    sched_week = []
    for i in range(7):
        sched_week.append(schedule_day(nurses_num, max_shifts_num))
    return sched_week



def uniform_crossover(A, B, P):
    c1 = A.deepcopy()
    c2 = B.deepcopy()
    c1week = c1.schedule
    c2week = c2.schedule
    for i in range(len(c1week)):
        temp = [0] * 9
        if P[0] < 0.5:
            temp[0:3] = c1week[i][0:3]
            c1week[i][0:3] = c2week[i][0:3]
            c2week[i][0:3] = temp[0:3]
        if P[1] < 0.5:
            temp[3:7] = c1week[i][3:7]
            c1week[i][3:7] = c2week[i][3:7]
            c2week[i][3:7] = temp[3:7]
        if P[2] < 0.5:
            temp[7:9] = c1week[i][7:9]
            c1week[i][7:9] = c2week[i][7:9]
            c2week[i][7:9] = temp[7:9]

    c1.schedule = c1week
    c2.schedule = c2week
    return c1, c2


def crossover(A, B, P):
    c1 = A.deepcopy()
    c2 = B.deepcopy()
    c1week = c1.schedule
    c2week = c2.schedule
    for i in range(len(c1week)):
        temp = [0] * 9
        if P[0] < 0.5:
            temp[0:3] = c1week[i][0:3]
            c1week[i][0:3] = c2week[i][0:3]
            c2week[i][0:3] = temp[0:3]
        if P[1] < 0.5:
            temp[3:7] = c1week[i][3:7]
            c1week[i][3:7] = c2week[i][3:7]
            c2week[i][3:7] = temp[3:7]
        if P[2] < 0.5:
            temp[7:9] = c1week[i][7:9]
            c1week[i][7:9] = c2week[i][7:9]
            c2week[i][7:9] = temp[7:9]

    c1.schedule = c1week
    c2.schedule = c2week
    return c1, c2


def mutate(p, mu):
    res = p.deepcopy()
    flag = np.random.rand(7) <= mu
    for i in range(len(flag)):
        if flag[i]:
            n1 = np.random.randint(0, 9)
            n2 = np.random.randint(0, 9)
            tmp = res.schedule[i][n1]
            res.schedule[i][n1] = res.schedule[i][n2]
            res.schedule[i][n2] = tmp
    return res



def run(problem, params):
    
    # problem
    fitness_func = problem.fitess_func
    nurses_num = problem.nurses_num
    max_shifts_num = problem.max_shifts_num


    # parameters
    npop = params.npop # population number
    maxit = params.maxit # maximum number of iterations
    pc = params.pc # children population
    mu = params.mu # mutation probability
    # nc is the number of children, which is pc times the number of parents
    # first divided by 2 and rounded, then multiplied by 2 to ensure that nc is an even number
    nc = int(np.round(pc*npop/2)*2) 

    # empty chromosome
    empty_chromosome = structure()
    empty_chromosome.fitness = None
    empty_chromosome.schedule = None

    # best solution
    best_chromosome = empty_chromosome.deepcopy()
    best_chromosome.fitness = 0

    # worst solution
    worst_chromosome = empty_chromosome.deepcopy()
    worst_chromosome.fitness = np.inf

    # initalizing population
    pop = empty_chromosome.repeat(npop)
    for i in range(npop):
        pop[i].schedule = schedule_week(nurses_num, max_shifts_num)
        pop[i].fitness = fitness_func(pop[i].schedule)

        if pop[i].fitness >= best_chromosome.fitness:
            best_chromosome = pop[i].deepcopy()
            
        if pop[i].fitness <= worst_chromosome.fitness:
            worst_chromosome = pop[i].deepcopy()

    print("Initial Population:")
    avg_fitness = sum(p.fitness for p in pop)/npop
    print("{identity:<7} Chromosome: fitness = {fitness:.8f}".format(identity="Best", fitness=best_chromosome.fitness))
    print("{identity:<7} Chromosome: fitness = {fitness:.8f}".format(identity="Worst", fitness=worst_chromosome.fitness))
    print("{identity:<7} Chromosome: fitness = {fitness:.8f}".format(identity="Average", fitness=avg_fitness))
    print("\n")

    # best cost of iterations
    bestcost = np.empty(maxit)

    # main loop
    for it in range(maxit):

        popc = []

        # parent selection, crossover, and mutation
        for k in range(nc//2):

            # select parents
            q = np.random.permutation(npop) # a random permutation from integers 0 to npop - 1
            p1 = pop[q[0]] # random first parent
            p2 = pop[q[1]] # random second parent

            # perform corssover
            p = np.random.rand(3)
            c1, c2 = uniform_crossover(p1, p2, p)

            # evaluate first offspring
            c1.fitness = fitness_func(c1.schedule)

            if c1.fitness >= best_chromosome.fitness:
                best_chromosome = c1.deepcopy()
            
            if c1.fitness <= worst_chromosome.fitness:
                worst_chromosome = c1.deepcopy()

            # evaluate second offspring
            c2.fitness = fitness_func(c2.schedule)

            if c2.fitness >= best_chromosome.fitness:
                best_chromosome = c2.deepcopy()
            
            if c2.fitness <= worst_chromosome.fitness:
                worst_chromosome = c2.deepcopy()

            # mutation
            c1 = mutate(c1, mu)
            c2 = mutate(c2, mu)


            # add offsprings to popc
            popc.append(c1)
            popc.append(c2)

        # merge, sort, and select
        pop += popc # Lambda, mu selection
        pop = sorted(pop, key=lambda p: p.fitness, reverse=True)
        pop = pop[0:npop] # top npop population

        # store best cost
        bestcost[it] = best_chromosome.cost

        # print information
        avg_fitness = sum(p.fitness for p in pop)/npop
        print("Iteration:", it)
        print("{identity:<7} Chromosome: fitness = {fitness:.8f}".format(identity="Best", fitness=best_chromosome.fitness))
        print("{identity:<7} Chromosome: fitness = {fitness:.8f}".format(identity="Worst", fitness=worst_chromosome.fitness))
        print("{identity:<7} Chromosome: fitness = {fitness:.8f}".format(identity="Average", fitness=avg_fitness))
        print("\n")

        if(best_chromosome.fitness == 250):
            break

    print("\nOutput:")
    result = []
    string_output = ""
    for sched_day in best_chromosome.schedule:
        shift1 = sched_day[0:3]
        shift1 = [i for i in shift1 if i!=0]
        shift2 = sched_day[3:7]
        shift2 = [i for i in shift2 if i!=0]
        shift3 = sched_day[7:9]
        shift3 = [i for i in shift3 if i!=0]
        day_res = []
        day_res.append(shift1)
        day_res.append(shift2)
        day_res.append(shift3)
        result.append(day_res)
        for shift in day_res:
            string_output += ','.join(map(str, shift))
            string_output += " "
        string_output += "\n"
    print(string_output)
    



    # output
    out = structure()
    out.pop = pop
    return out
