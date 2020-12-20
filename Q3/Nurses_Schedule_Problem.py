import math
from ypstruct import structure
import numpy as np
import GA

NURSES_NUM = 8

def fitness_func(sched_week):
    fitness = 0
    stage1_score = max_stage1_score = 70
    for sched_day in sched_week:
        shift1 = sched_day[0:3]
        shift2 = sched_day[3:7]
        shift3 = sched_day[3:7]
        negative_score1 = sum(el in shift1 for el in shift2)
        negative_score2 = sum(el in shift2 for el in shift3)
        stage1_score = stage1_score - (negative_score1 + negative_score2)

    stage2_score = max_stage2_score = 150
    nurse_shifts_num = [0] * (NURSES_NUM+1)
    for i in range(1, NURSES_NUM+1):
        for sched_day in sched_week:
            nurse_shifts_num[i] += sched_day.count(i)

    for num in nurse_shifts_num:
        if num > 5:
            stage2_score = stage2_score - (num - 5) * 5
    
    fitness = stage1_score + stage2_score
    return fitness


def main():

    # Defining the problem
    problem = structure()
    problem.fitess_func = fitness_func
    problem.nurses_num = NURSES_NUM
    problem.max_shifts_num = 9 # maximum number of shifts in each day

    # Defining the parameters
    params = structure()
    params.npop = 100 # ancestors population number
    params.pc = 4*params.npop # children population number
    params.maxit = 30 # maximum number of iterations
    params.mu = 0.2 # mutation probability
    
    # running the GA algorithm
    GA.run(problem, params)


if __name__ == '__main__':
    main()