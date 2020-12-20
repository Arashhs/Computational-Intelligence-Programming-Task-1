import math
from ypstruct import structure
import numpy as np
import ES

GLOBAL_MIN = -959.6407

def eggholder_func(x):
    x1 = x[0]
    x2 = x[1]
    term1 = -(x2+47) * math.sin(math.sqrt(abs(x2+x1/2+47)))
    term2 = x1 * math.sin(math.sqrt(abs(x1-(x2+47))))
    res = term1 - term2
    return res


def fitness_func(f):
    term = abs(f-GLOBAL_MIN)
    # handling the case when f = 0 since division by 0 is undefined
    fitness = 1 / term if term != 0 else np.inf
    return fitness




def main():

    # Defining the problem
    problem = structure()
    problem.eggholder_func = eggholder_func
    problem.fitess_func = fitness_func
    problem.nvar = 2
    problem.varmin = -512
    problem.varmax = 512

    # Defining the parameters
    params = structure()
    params.npop = 40 # ancestors population number
    params.pc = 5*params.npop # children population number
    params.maxit = 30 # maximum number of iterations
    params.sigma = 0.6 # learning rate
    params.gamma = 0.01
    

    # running the GA algorithm
    ES.run(problem, params)


if __name__ == '__main__':
    main()