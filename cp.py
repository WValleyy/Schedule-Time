from ortools.sat.python import cp_model

# Create input
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

cla_sub_teacher = [set() for i in range(T+1)]
tea_sub = [set() for i in range(N+1)]
for t in teacher:
    tea = teacher[t]
    for x in class_sub:
        subject = class_sub[x]
        for y in subject:
            if y in tea :
                cla_sub_teacher[t].add((x,y))
                tea_sub[x].add((t,y))

# Modelling

model = cp_model.CpModel()
Period = 6
Session = 10

# Creates Schedule variables.
# Schedule[(t, c, p, s)]: Teacher {t} teach class {x} subject {y} at period {u} in session {s}.
Schedule = {}
for t in teacher:
    cla_sub = cla_sub_teacher[t]
    for (x,y) in cla_sub:
        for s in range(1, Session+1):
            for u in range(1, Period+1):

                    Schedule[(t, x, y, u, s)] = model.NewBoolVar(f'Schedule {t} {x} {y} {u} {s}')

# Create constraints

# Each teacher teach atmost 1 class in 1 period
for t in teacher:
    cla_sub = cla_sub_teacher[t]
    for s in range(1, Session+1):
        for u in range(1, Period+1):

            model.AddAtMostOne(Schedule[(t, x, y, u, s)] for (x,y) in cla_sub)

# Each class can learn atmost 1 subject in 1 period
for x in class_sub:
    t_sub =  tea_sub[x]
    for s in range(1, Session+1):
        for u in range(1, Period+1):
            
            model.AddAtMostOne(Schedule[(t, x, y, u, s)] for (t,y) in t_sub)


# Each class-sub can learn max once time a week 
for x in class_sub:
    subject = class_sub[x]
    for y in subject:                
        model.Add(sum(Schedule[(t, x, y, u, s)] 
        for s in range(1, Session+1) for u in range(1, Period+1)
        for t in teacher if y in teacher[t]) <= period_sub[y])
            

# The periods of the class-subject must be adjacent
for s in range(1, Session+1):   
    for t in teacher:
        cla_sub = cla_sub_teacher[t]
        for (x,y) in cla_sub:
                    pe = period_sub[y]
                    
                    model.Add(sum(Schedule[(t, x, y, u_, s)]
                            for u_ in range(1, 1+pe)) == pe).OnlyEnforceIf(Schedule[(t, x, y, 1, s)])

                    for u in range(2,Period+2-pe):  
                            model.Add(sum(Schedule[(t, x, y, u_, s)] 
                            for u_ in range(u,u+pe)) == pe).OnlyEnforceIf(Schedule[(t, x, y, u, s)],Schedule[(t, x, y, u-1, s)].Not())
                            
# Each class-subject learn full or 0 period in each session                        
for s in range(1, Session+1):
    for t in teacher:
        for (x,y) in cla_sub_teacher[t]:
            pe = period_sub[y]
            teach = model.NewBoolVar('t')
            model.Add(sum(Schedule[(t, x, y, u, s)] for u in range(1, Period+1)) == pe).OnlyEnforceIf(teach)
            model.Add(sum(Schedule[(t, x, y, u, s)] for u in range(1, Period+1)) == 0).OnlyEnforceIf(teach.Not())



# Objective function
model.Maximize(sum(Schedule[(t, x, y, u, s)] for t in teacher for (x,y) in cla_sub_teacher[t] for u in range(1,Period+1) for s in range(1,Session+1)))

# Solver
solver = cp_model.CpSolver()

status = solver.Solve(model)
count = 0
sol =[]

def Solution(t, x, y, s):
    global count
    for u in range(1, Period + 1):
        
        if solver.Value(Schedule[(t, x, y, u, s)]):
                                    
            count += 1
            return [x,y,u+(s-1)*6,t]
    return None

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    for t in teacher:
        cla_sub = cla_sub_teacher[t]
        for (x,y) in cla_sub:
            for s in range(1,Session+1):
                    z = Solution(t, x, y, s)
                    if z != None:
                        sol.append(z)
                
else:
    print('No solution found.')

def PrintSolution():
    print(count)
    for x in sol:
        for i in x:
            print(i,end=' ')
        print()
PrintSolution()
