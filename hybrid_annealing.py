import random
import math
import copy
import sys

# Create input
teacher= {}
class_sub = {}
period_sub = {}
period = 6
session = 10
[T, N, M] = [int(x) for x in sys.stdin.readline().split()]
for i in range(1, N+1):
        class_sub[i] ={int(x) for x in sys.stdin.readline().split()[:-1]}
for j in range(N+1, T+N+1):
        teacher[j-N] = {int(x) for x in sys.stdin.readline().split()[:-1]}
period_sub = [int(x) for x in sys.stdin.readline().split()]
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

#Construct list of Sub-class
C_s_p = [] #list of class_subject_periods
Timetable = [[0 for sessons in range(session+1)] for room in range(N+1)]
# Timetable is the timetable for all class each is built by the start period of each sessons
for c in class_sub:
    for sub in class_sub[c]:
        p = period_sub[sub]
        C_s_p.append((sub,c,p)) #Containing subject-class-period in a list
        
C_s_p= sorted(C_s_p, key = lambda x: x[2],reverse = True)
teacher_list = [] # construct teacher PriorityQueue
for t in teacher:
    teacher_list.append((0,t,[0 for sessons in range(session+1)])) 
    # Containing number of periods that teacher teach, name, timetable for that teacher
    # Timetable for teacher is built by the start period of each sessons 
    
def select(name_teacher,classes_teacher):
    # Select the first sub-class that satisfies the condition and the start period of 
    # classes and teacher must be the same
    global C_s_p
    for y in C_s_p:

        if (y[0] in teacher[name_teacher]):
            for i in range(1,session+1):
                 if (Timetable[y[1]][i]+y[2]<=6) and (classes_teacher[i]+y[2]<=6) and Timetable[y[1]][i] == classes_teacher[i]:

                     Timetable[y[1]][i] = Timetable[y[1]][i]+y[2] #update start periods classes 
                     classes_teacher[i] = classes_teacher[i]+y[2]

                     return y,(Timetable[y[1]][i]-y[2]+1,i),classes_teacher # teacher, start period, teacher_period
    return None,None,None

def select2(name_teacher,classes_teacher):
    # Select the first sub-class that satisfies the condition and the start period of 
    # classes and teacher must be the same
    global C_s_p
    for y in C_s_p:

        if (y[0] in teacher[name_teacher]):
            for i in range(1,session+1):
                 if (Timetable[y[1]][i]+y[2]<=6) and (classes_teacher[i]+y[2]<=6) :
                    if Timetable[y[1]][i] >= classes_teacher[i]:
                        classes_teacher[i] = Timetable[y[1]][i]+y[2]
                        Timetable[y[1]][i] = Timetable[y[1]][i]+y[2]
                    else:
                        Timetable[y[1]][i] = classes_teacher[i]+y[2]
                        classes_teacher[i] = classes_teacher[i]+y[2]
                    return y,(Timetable[y[1]][i]-y[2]+1,i),classes_teacher  # teacher, start period, teacher_period
    return None,None,None  

def Greedy():
    global C_s_p
    Class_sub_sastify = [] # list of sastify class - sub - start classes - teacher
    # start classes for teacher in each session
    # start classes for room in each session
    
    while len(C_s_p)>0:
        temp = [] # remember the updated teacher
        check=[] #teacher that has already checked
        while not teacher_list == []:        
            t = teacher_list.pop()
            check.append(t)
            x,s,c_t = select(t[1],t[2])
            if x==None:
                temp.append(t)
                continue 
            Class_sub_sastify.append((x[1],x[0],s[0]+6*(s[1]-1),t[1]))
            C_s_p.remove(x)                
            temp.append((t[0]+x[2],t[1],c_t)) #update teacher_period
        if check==temp: # no more changes on teacher that can teach 
            for t in temp:
                teacher_list.append(t) # update the teacher queue for improvedGreedy
            return Class_sub_sastify
        for t in temp:
            teacher_list.append(t) # update the teacher queue for next iteration     
    return Class_sub_sastify

def improvedGreedy():
    global C_s_p
    Class_sub_sastify = [] # list of sastify class - sub - start classes - teacher
    # start classes for teacher in each session
    # start classes for room in each session    
    while len(C_s_p)>0:
         # Timetable classes that have already scheduled (in current iteration)
        temp = []
        check=[]
        while not teacher_list == []:        
            t = teacher_list.pop()
            check.append(t)        
            x,s,c_t = select2(t[1],t[2])
            if x==None:
                temp.append(t)
                continue 
            Class_sub_sastify.append((x[1],x[0],s[0]+6*(s[1]-1),t[1])) # append solution in list
            C_s_p.remove(x)
            temp.append((t[0]+x[2],t[1],c_t)) #update teacher_period
        if check==temp: # no more change can make on teacher
            return Class_sub_sastify
        for t in temp:
            teacher_list.append(t) #update teacher_list for next interation     
    return Class_sub_sastify


def initialize_greedy():
    cs = []
    for c in class_sub:
        for s in class_sub[c]:
            cs.append((c,s))
    
    S1 = Greedy()
    S2 = improvedGreedy()
    s=[]
    s=S1+S2
    s.sort()
    schedule = []
    
    for (c,sub,p,t) in s:
        schedule.append([sub,c,t,p//6 +1,p%6,p%6 + period_sub[sub]])
        #schedule.append([sub,c,0,0,0,0])
        cs.remove((c,sub))
    for (c,s) in cs:
        schedule.append([s,c,0,0,0,0])
    return schedule

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
    e = [0 for i in range(51)]
    for x in schedule:
        if x[2] != 0:
            evaluate += 1
            e[x[3]] = e[x[3]] + 1
    for i in range(1,51):
        if e[i] >= 0.8*T:
            evaluate += 1
    return evaluate 

def count_class(schedule):
    evaluate = 0
    for x in schedule:
        if x[2] != 0:
            evaluate += 1
    return evaluate 

def neighborhood(schedule): #to list all posstible moves
    nbhood = []
    temp = copy.deepcopy(schedule)
    for i in range(len(temp)):
        if temp[i][2] != 0:
            x = temp[i]
            t = temp[i][:]
            #drop
            nbhood.append(('drop',x[0],x[1]))
            temp[i] = t
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
                            nbhood.append(('assign',x[0],x[1],\
                            teach,part,start,start + period_sub[temp[i][0]] ))
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
    
    elif choice[0] == 'move':
        for x in temp:
            if x[0] == choice[1] and x[1] == choice[2]:
                x[4] = choice[3]
                x[5] = choice[3] + period_sub[x[0]]
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
    for i in range(20):
        for j in range(50):
            nb = select_random_neighbor(current)
            current = nb
            current_fitness = fitness_function(current)
            E = abs(current_fitness - best_fitness)
            if current_fitness <= best_fitness:
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
        record_best_fit.append(best_fitness)
        temperature = temperature/(1+i)
    return best_solution

init_solution = initialize_greedy()
solution = simulated_annealing(init_solution, 100)
count = 0
for x in solution:
    if x[2] != 0:
        count+=1
print(count)
for x in solution:
    if x[2] != 0:
        print(str(x[1])+' '+str(x[0])+' '+str(6*(x[3]-1)+x[4])+' '+str(x[2]))
