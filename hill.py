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
        if temp[i][2] ==0:
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
    if len(neighborhood(schedule)) == 0:
        return None
    choice = random.choice(neighborhood(schedule))
    for x in temp:
        if x[0] == choice[1] and x[1] == choice[2]:
            x[2] = choice[3]
            x[3] = choice[4]
            x[4] = choice[5]
            x[5] = choice[6]
            return temp

def simple_hill_climbing(schedule):
    current = copy.deepcopy(schedule)
    current_fit = fitness_function(current)
    neighbor = select_random_neighbor(current)
    neighbor_fit = fitness_function(neighbor)
    count = 0
    while neighbor_fit >= current_fit:
        count+=1
        current = neighbor
        neighbor = select_random_neighbor(neighbor)
        if neighbor == None:
            break
        current_fit = fitness_function(current)
        neighbor_fit = fitness_function(neighbor)
        print('iteration',count,'best fitness',current_fit)
    return current

print('initial fitness',fitness_function(init_solution))
solution = simple_hill_climbing(init_solution)

print(fitness_function(solution))

count = 0
for x in solution:
    if x[2] != 0:
        count+=1

with open("outp.txt", "w") as f:
    f.write(str(count)+'\n')
    for x in solution:
        if x[2] != 0:
            f.write(str(x[1])+' '+str(x[0])+' '+str(6*(x[3]-1)+x[4])+' '+str(x[2])+'\n')
        