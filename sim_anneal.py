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

print(class_sub)
print(teacher)
period_sub.insert(0,0)
print(period_sub)
print(course)

#Using greedy1 to make a feasible initial solution
#Construct list of C and priority
C = []
mark = [[0 for sessons in range(11)] for room in range(N+1)]
for c in class_sub:
    for sub in class_sub[c]:
        p = period_sub[sub]
        C.append((sub,c,p)) #containing subject-class tuples
        
C= sorted(C, key = lambda x: x[2],reverse = True)
teacher_queue = PriorityQueue()
for t in teacher:
    teacher_queue.put((0,t,[0 for sessons in range(11)]))


def select(name_teacher,classes_teacher):
    global C
    for y in C:

        if (y[0] in teacher[name_teacher]):
            for i in range(1,11):
                 if (mark[y[1]][i]+y[2]<=6) and (classes_teacher[i]+y[2]<=6) and mark[y[1]][i] == classes_teacher[i]:

                     mark[y[1]][i] = mark[y[1]][i]+y[2]
                     classes_teacher[i] = classes_teacher[i]+y[2]

                     return y,(mark[y[1]][i]-y[2]+1,i),classes_teacher
    #print('cant select s-c for teacher',t,candidates)

    return None,None,None

def Greedy():
    global C
    S = []
    # start classes for teacher in each session
    # start classes for room in each session
    
    while len(C)>0:
         # mark classes that have already scheduled (in current iteration)
        temp = []
        check=[]
        while not teacher_queue.empty():
        
            t = teacher_queue.get()
            check.append(t)
        #print('run here',t[0],t[1])
            x,s,c_t = select(t[1],t[2])
            if x==None:
                temp.append(t)

                continue 
                #continue
            S.append((x[1],x[0],s[0]+6*(s[1]-1),t[1]))
            C.remove(x)
                #print(t[0],t[1],x[3],c_t)
                #temp.append((t[0]+x[3],t[1],c_t))
            temp.append((t[0]+x[2],t[1],c_t))
        if check==temp:
            for t in temp:
                teacher_queue.put(t) 
            return S
        for t in temp:
            teacher_queue.put(t) 
     
    return S

cs = []
for c in class_sub:
    for s in class_sub[c]:
        cs.append((c,s))
def initialize():
    s = Greedy()
    schedule = []
    
    for (c,sub,p,t) in s:
        schedule.append([sub,c,t,p//6 +1,p%6,p%6 + period_sub[sub]])
        #schedule.append([sub,c,0,0,0,0])
        cs.remove((c,sub))
    for (c,s) in cs:
        schedule.append([s,c,0,0,0,0])
    return schedule
init_solution = initialize()
print(init_solution)

def condition_check(schedule):
    #check overlap conditions
    #other conditions are already satisfied
    evaluate = 0
    for i in range(len(schedule)):
        for j in range(i+1,len(schedule)):
            if (schedule[i][1] == schedule[j][1]) and (schedule[i][3] == schedule[j][3]):
                #same class in one part -> cannot overlap
                if schedule[i][4] in range(schedule[j][4],schedule[j][5]) or schedule[j][4] in range(schedule[i][4],schedule[i][5]):
                    evaluate -= 1
            if (schedule[i][2] == schedule[j][2]) and (schedule[i][3] == schedule[j][3]):
                #same teacher in one part -> cannot overlap
                if schedule[i][4] in range(schedule[j][4],schedule[j][5]) or schedule[j][4] in range(schedule[i][4],schedule[i][5]):
                    evaluate -= 1
    return evaluate

def fitness_function(schedule): #number of class-sub assigned
    evaluate = 0
    for x in schedule:
        if x[2] != 0:
            evaluate +=1
    return evaluate

def neighborhood(schedule): #to list all posstible moves
    #if has no violations -> append to nbhood list
    nbhood = []
    temp = copy.deepcopy(schedule)

    for i in range(len(temp)):
        if temp[i][2] != 0:
            x = temp[i]
            t = temp[i][:]
            #change in position
            for start in range(1,temp[i][4]):
                x[4] = start
                x[5] = start + period_sub[temp[i][0]] 
                if condition_check(temp) == 0:
                    nbhood.append(copy.deepcopy(temp))

            for start in range(temp[i][4]+1,8-period_sub[temp[i][0]]):
                x[4] = start
                x[5] = start + period_sub[temp[i][0]] 
                if condition_check(temp) == 0:
                    nbhood.append(copy.deepcopy(temp))
            # drop some assigned classes
            x[2] = 0
            x[3] = 0
            x[4] = 0
            x[5] = 0
            nbhood.append(copy.deepcopy(temp))
            temp[i] = t
            # move some assigned classes in their blocks (change starting points)
            

        else: # assign some classes
            for part in range(1,11):
                for start in range(1,7):
                    t = temp[i][:]
                    x = temp[i]
                    for teach in course[temp[i][0]]:
                        x[2] = teach
                        x[3] = part
                        x[4] = start
                        x[5] = start + period_sub[temp[i][0]] 
                        if condition_check(temp) == 0:
                            
                            nbhood.append(copy.deepcopy(temp))
                    temp[i] = t
    return nbhood

def select_random_neighbor(schedule):
    return random.choice(neighborhood(schedule))


def simulated_annealing(schedule, temperature):
    global record_best_fit
    current = copy.deepcopy(schedule)
    best_fitness = fitness_function(current)
    record_best_fit = list()
    n = 1#count solution accepted
    for i in range(50):
        for j in range(20):
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
        print("iteration:{}, best solution:{}, best fitness:{}".format(i, best_solution, best_fitness))
        record_best_fit.append(best_fitness)
        temperature = temperature/(1+i)
    return best_solution

solution = simulated_annealing(init_solution, 100)
print(fitness_function(init_solution))
print(fitness_function(solution))

