import math
from ypstruct import structure
import numpy as np
import GA

NURSES_NUM = 8

def fitness_func(sched_week):
    fitness = 0
    stage1_score = max_stage1_score = 50
    for sched_day in sched_week:
        shift1 = sched_day[0:3]
        shift2 = sched_day[3:7]
        shift3 = sched_day[7:9]
        for i in shift1:
            if i in shift2 and i != 0:
                stage1_score -= 10
        for i in shift2:
            if i in shift3 and i != 0:
                stage1_score -= 10

    stage2_score = max_stage2_score = 100
    nurse_shifts_num = [0] * (NURSES_NUM+1)
    for i in range(1, NURSES_NUM+1):
        for sched_day in sched_week:
            nurse_shifts_num[i] += sched_day.count(i)

    for num in nurse_shifts_num:
        if num > 5:
            stage2_score = stage2_score - (num - 5) * 5

    stage3_score = max_stage3_score = 100
    for sched_day in sched_week:
        shift1 = sched_day[0:3]
        shift2 = sched_day[3:7]
        shift3 = sched_day[7:9]
        n1 = shift1.count(0)
        if n1 > 1:
            stage3_score -= (10*(n1-1))
        n2 = shift2.count(0)
        if n2 > 2:
            stage3_score -= (10*(n2-2))
        n3 = shift3.count(0)
        if n3 == 2:
            stage3_score -= 10

    
    stage4_score = max_stage4_score = 100
    for sched_day in sched_week:
        shift1 = sched_day[0:3]
        shift2 = sched_day[3:7]
        shift3 = sched_day[7:9]
        duplicates = 0
        for i in shift1:
            if i != 0:
                duplicates += (shift1.count(i) - 1)
        for i in shift2:
            if i != 0:
                duplicates += (shift2.count(i) - 1)
        for i in shift3:
            if i != 0:
                duplicates += (shift3.count(i) - 1)
        stage4_score -= (duplicates*10)
        #print(duplicates, shift1, shift2, shift3)
        
    fitness = stage1_score + stage2_score + stage3_score + stage4_score
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
    params.pc = 1*params.npop # children population number
    params.maxit = 100 # maximum number of iterations
    params.mu = 0.4 # mutation probability
    
    # running the GA algorithm
    GA.run(problem, params)


if __name__ == '__main__':
    main()