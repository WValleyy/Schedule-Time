from VarIntLS import VarIntLS
from LocalSearchManager import LocalSearchManager 
from NotEqual import NotEqual
from NotEqualFunction import NotEqualFunction
from LessOrEqualFunctionConst import LessOrEqualFunctionConst
from AllDifferentFunction import AllDifferentFunction 
from ConstraintSystem import ConstraintSystem
from PlusVarConst import PlusVarConst
from HillClimbingSearch import HillClimbingSearch 
from ConditionalSum import ConditionalSum
import random as rd

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


print(class_sub)
print(teacher)
period_sub.insert(0,0)
print(period_sub)

mgr = LocalSearchManager()
Period = 5
Session = 10
Schedule = {}

for t in teacher:
    subject = teacher[t]
    for c in class_sub:
        for p in range (1, Period+1):
            for s in range (1, Session+1):
                for sub in subject:
                    if sub in class_sub[c]:
                        Schedule[(t,c,sub,p,s)] = VarIntLS(mgr,0,1,0,f'Schedule {t} {c} {sub} {p} {s}')

constraints = []
#Each class has <=1 subject at one time:
for c in class_sub:
    for s in range(1, Session+1):
        for p in range(1, Period+1):
            f = ConditionalSum([Schedule[(t, c, sub, p, s)] for sub in class_sub[c] for t in teacher if sub in teacher[t]],
            [1 for sub in class_sub[c] for t in teacher if sub in teacher[t]],1,'conditionalsum')
            constraints.append(LessOrEqualFunctionConst(f,1,'le'))
#Each teacher has <=1 subject at one time:
for t in teacher:
    for s in range(1, Session+1):
        for p in range(1, Period+1):
            f = ConditionalSum([Schedule[(t, c, sub, p, s)] for sub in teacher[t] for c in class_sub if sub in class_sub[c]],
            [1 for sub in teacher[t] for c in class_sub if sub in class_sub[c]],1,'conditionalsum')
            constraints.append(LessOrEqualFunctionConst(f,1,'le'))
#completely learn all courses in a class-sub:
for c in class_sub:
    subject = class_sub[c]
    for sub in subject:
        f = ConditionalSum([Schedule[(t, c, sub, p, s)] for s in range(1, Session+1) for p in range(1, Period+1) for t in teacher if sub in teacher[t]],
        [1 for s in range(1, Session+1) for p in range(1, Period+1) for t in teacher if sub in teacher[t]],1,'conditionalsum')
        constraints.append(LessOrEqualFunctionConst(f,period_sub[sub],'le'))
        f = ConditionalSum([Schedule[(t, c, sub, p, s)] for s in range(1, Session+1) for p in range(1, Period+1) for t in teacher if sub in teacher[t]],
        [-1 for s in range(1, Session+1) for p in range(1, Period+1) for t in teacher if sub in teacher[t]],1,'conditionalsum')
        constraints.append(LessOrEqualFunctionConst(f,-period_sub[sub],'le'))

C = ConstraintSystem(constraints)
mgr.close() #close the model

def printSolution():
    print('solution:')
    for s in range(1, Session+1):
        print('Session ' + str(s))
        for p in range(1,Period + 1):         
            for t in teacher:
                for c in class_sub:
                    for sub in teacher[t]:
                        if sub in class_sub:
                            if Schedule[(t, c, sub, p, s)].getValue():
                                print('Teacher ' + str(t) + ' teach class ' +
                                        str(c) + ' the subject ' + str(sub) + ' at period ' + str(p))
                            
    print(C.violations(),'violations')

for iters in range(2000):
    candidates = []
    minDelta = 1e9
    for c in class_sub:
        for p in range (1, Period+1):
            for s in range (1, Session+1):
                for t in teacher:
                    subject = teacher[t]
                    for sub in subject:
                        if sub in class_sub[c]:
                            delta = C.getAssignDelta(Schedule[(t,c,sub,p,s)],1)
                            if delta < minDelta:
                                minDelta = delta
                                candidates = []
                                candidates.append((t,c,sub,p,s))
                            elif delta == minDelta:
                                candidates.append((t,c,sub,p,s))
    idx = rd.randint(0,len(candidates)-1)
    if candidates[idx] == 0:
        print('stay')
    else:
        address = candidates[idx]
        Schedule[address].setValuePropagate(1)
        print('step',iters,'violates',C.violations())        

    if C.violations() == 0:
        break   

printSolution()     
                        
    