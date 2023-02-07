import random
import math
import copy
from queue import PriorityQueue
# Create input

teacher= {}
class_sub = {}
period_sub = {}

with open("data.txt", "r") as f:
    lines = f.readlines()
    T, N, M = [int(x) for x in lines[0].split()]
    for i in range(1, N+1):
        class_sub[i] =set(map(int,lines[i].split()[:-1]))
    for j in range(N+1, T+N+1):
        teacher[j-N] = set(map(int,lines[j].split()[:-1]))
    period_sub = list(map(int,lines[T+N+1].split()))

course = [[] for i in range(M+1)]
for sub in range(1,M+1):
    for t in teacher:
        if sub in teacher[t]:
            course[sub].append(t) 

period_sub.insert(0,0)

def initialize():
    cs = []
    for c in class_sub:
        for s in class_sub[c]:
            cs.append([s,c,0,0,0,0])
            #elements of the schedule are in the form of: 
            # [subject, class, teacher, part, start, end]

            
    return cs
init_solution = initialize()

def condition_check(schedule,part): #better O(n) 
    mark_teacher = [[False for j in range(T+1)] for i in range(7)]
    mark_class = [[False for j in range(N+1)]for i in range(7)]
    for i in range(len(schedule)):
        if schedule[i][3] == part:
            for j in range(schedule[i][4],schedule[i][5]):
                if mark_teacher[j][schedule[i][2]]:
                    return False
                mark_teacher[j][schedule[i][2]] = True
                if mark_class[j][schedule[i][1]]:
                    return False
                mark_class[j][schedule[i][1]] = True
    return True

def fitness_function(schedule): #number of class-sub assigned
    evaluate = 0
    for x in schedule:
        if x[2] != 0:
            evaluate += 1

    return evaluate 

def neighborhood(schedule): #to list all posstible moves
    nbhood = []
    temp = copy.deepcopy(schedule)
    count_sol = 0
    for i in range(len(temp)):
        if temp[i][2] != 0:
            nbhood.append(('drop',temp[i][0],temp[i][1]))
        else: # assign some unassigned classes
            t = temp[i][:]
            x = temp[i]
            for part in range(1,11):
                for start in range(1,8 - period_sub[temp[i][0]]):
                    for teach in course[temp[i][0]]:
                        x[2] = teach
                        x[3] = part
                        x[4] = start
                        x[5] = start + period_sub[temp[i][0]] 
                        if condition_check(temp,temp[i][3]):
                            nbhood.append(('assign',x[0],x[1],teach,part,start,start + period_sub[temp[i][0]] ))
            temp[i] = t
    return nbhood

def select_random_neighbor(schedule):
    temp = copy.deepcopy(schedule)
    choice = random.choice(neighborhood(schedule))
    if choice[0] == 'drop':
        for x in temp:
            if x[0] == choice[1] and x[1] == choice[2]:
                x[2] = 0
                x[3] = 0
                x[4] = 0
                x[5] = 0
                return temp
    else:
        for x in temp:
            if x[0] == choice[1] and x[1] == choice[2]:
                x[2] = choice[3]
                x[3] = choice[4]
                x[4] = choice[5]
                x[5] = choice[6]
                return temp

def simulated_annealing(schedule, temperature):
    global record_best_fit
    current = copy.deepcopy(schedule)
    best_fitness = fitness_function(current)
    record_best_fit = list()
    n = 1#count solution accepted
    for i in range(50):
        for j in range(50):
            nb = select_random_neighbor(current)
            current = nb
            current_fitness = fitness_function(current)
            E = abs(current_fitness - best_fitness)
            if current_fitness < best_fitness:
                if temperature == 0: #temperature get near 0 -> dont accept
                    continue
                else:
                    p = math.exp(-E/temperature)
                if random.random() < p:
                    accept = True
                else:
                    accept = False
            else:
                accept = True
            if accept == True:
                best_solution = copy.deepcopy(current)
                best_fitness = fitness_function(best_solution)
                record_best_fit.append(best_fitness)
                n += 1
                #print("small iteration:{}, best solution:{}, best fitness:{}".format(j, best_solution, best_fitness))
        print("iteration:{}, best fitness:{}".format(i, best_fitness))
        record_best_fit.append(best_fitness)
        temperature = temperature/(1+i)
    return best_solution

print('initial fitness',fitness_function(init_solution))
solution = simulated_annealing(init_solution, 200)

print('initial fitness', fitness_function(solution))

count = 0
for x in solution:
    if x[2] != 0:
        count+=1

with open("outp.txt", "w") as f:
    f.write(str(count)+'\n')
    for x in solution:
        if x[2] != 0:
            f.write(str(x[1])+' '+str(x[0])+' '+str(6*(x[3]-1)+x[4])+' '+str(x[2])+'\n')
        