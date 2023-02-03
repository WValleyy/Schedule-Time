from ortools.sat.python import cp_model
# Create input
import time
teacher= {}
class_sub = {}
period_sub = {}

with open('data.txt', "r") as f:
    lines = f.readlines()
    T, N, M = [int(x) for x in lines[0].split()]
    for i in range(1, N+1):
        class_sub[i] =set(map(int,lines[i].split()[:-1]))
    for j in range(N+1, T+N+1):
        teacher[j-N] = set(map(int,lines[j].split()[:-1]))
    period_sub = list(map(int,lines[T+N+1].split()))
period_sub.insert(0,0)

sub_teacher_can_teach = [[] for i in range(T+2)]
for t in teacher:
    tea = teacher[t]
    for c in class_sub:
        subject = class_sub[c]
        for sub in subject:
            if sub in tea :
                sub_teacher_can_teach[t].append((c,sub))


# Modelling

model = cp_model.CpModel()
Period = 6
Session = 10

# Creates Schedule variables.
# Schedule[(t, c, p, s)]: Teacher {t} teach class {c} subject {sub} at period {p} in session {s}.
Schedule = {}
for t in teacher:
    cla_sub = sub_teacher_can_teach[t]
    for (c,sub) in cla_sub:
        for s in range(1, Session+1):
            for p in range(1, Period+1):

                    Schedule[(t,c,sub,p,s)] = model.NewBoolVar(f'Schedule {t} {c} {sub} {p} {s}')

# Create constraints

# Teacher can only teach the class have the subject they can teach


# Each teacher teach atmost one class in 1 period
for t in teacher:
    cla_sub = sub_teacher_can_teach[t]
    for s in range(1, Session+1):
        for p in range(1, Period+1):

            model.AddAtMostOne(Schedule[(t, c, sub, p, s)] for (c,sub) in cla_sub)

# Each class can learn atmost one subject in 1 period
for c in class_sub:
    for s in range(1, Session+1):
        for p in range(1, Period+1):

            model.AddAtMostOne(Schedule[(t, c, sub, p, s)] for sub in class_sub[c] for t in teacher if sub in teacher[t])


# Each class-sub can learn max once time a week 
for c in class_sub:
    subject = class_sub[c]
    for sub in subject:
                        
        model.Add(sum(Schedule[(t, c, sub, p, s)] 
        for s in range(1, Session+1) for p in range(1, Period+1)
        for t in teacher if sub in teacher[t]) <= period_sub[sub])

# Each teacher teach exactly 1 class-sub, Subjects must to be teached done in 1 Session
for t in teacher:
    cla_sub = sub_teacher_can_teach[t]
    for (c,sub) in cla_sub:
        for s in range(1,Session+1):
                teach = model.NewBoolVar('t')
                sub_pe = sum(Schedule[(t, c, sub, p, s)] 
                for p in range(1, Period+1))

                model.Add(sub_pe == 0).OnlyEnforceIf(teach.Not())

                model.Add(sub_pe == period_sub[sub] ).OnlyEnforceIf(teach)

# The periods of the class-subject must be adjacent
for s in range(1, Session + 1):   
    for t in teacher:
        cla_sub = sub_teacher_can_teach[t]
        for (c,sub) in cla_sub:
                    pe = period_sub[sub]
                    model.Add(sum(Schedule[(t, c, sub, p_, s)]
                            for p_ in range(1,1+pe)) == pe).OnlyEnforceIf(Schedule[(t, c, sub, 1, s)]) 
                    for p in range(2,Period+2-pe):  

                            model.Add(sum(Schedule[(t, c, sub, p_, s)] 
                            for p_ in range(p,p+pe)) == pe).OnlyEnforceIf(Schedule[(t, c, sub, p, s)],Schedule[(t, c, sub, p-1, s)].Not())
                            



# Objective function
model.Maximize(sum(Schedule[(t, c, sub, p, s)] for t in teacher for sub in teacher[t] 
for c in class_sub if sub in class_sub[c] for p in range(1,Period+1) for s in range(1,Session+1)))

# Solver
solver = cp_model.CpSolver()
start_time = time.time()
status = solver.Solve(model)
end_time = time.time()
count = 0
sol =[]

def Solution(c,s,sub,t):
    global count
    for p in range(1, Period + 1):
        
        if solver.Value(Schedule[(t, c, sub, p, s)]):
                                    
                                    count += 1
                                    return [c,sub,p+(s-1)*6,t]
    return None

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    for s in range(1, Session+1):
        for c in class_sub:
            for sub in class_sub[c]:
                for t in teacher :
                    if sub in teacher[t]:
                        x = Solution(c,s,sub,t)
                        if x != None:
                            sol.append(x)
                
else:
    print('No solution found.')

def PrintSolution():
    print(count)
    for x in sol:
        for i in x:
            print(i,end=' ')
        print()

PrintSolution()
elapsed_time = end_time - start_time
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
