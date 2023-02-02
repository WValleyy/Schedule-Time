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

# Modelling

model = cp_model.CpModel()
Period = 6
Session = 10

# Creates Schedule variables.
# Schedule[(t, c, p, s)]: Teacher {t} teach class {c} subject {sub} at period {p} in session {s}.
Schedule = {}
for t in teacher:
    subject = teacher[t]
    for c in class_sub:
        for p in range (1, Period+1):
            for s in range (1, Session+1):
                for sub in subject:

                    Schedule[(t,c,sub,p,s)] = model.NewBoolVar(f'Schedule {t} {c} {sub} {p} {s}')

# Create constraints

# Teacher can only teach the class have the subject they can teach
for t in teacher:
    for s in range(1, Session+1):
        for p in range(1, Period+1):
            for c in class_sub:
                subject = class_sub[c]
                for sub_teach in teacher[t]:
 
                    model.Add(sub_teach in subject).OnlyEnforceIf(Schedule[(t, c, sub_teach, p, s)])


# Each teacher teach atmost one class in 1 period
for t in teacher:
    for s in range(1, Session+1):
        for p in range(1, Period+1):

            model.AddAtMostOne(Schedule[(t, c, sub, p, s)]  for sub in teacher[t] for c in class_sub if sub in class_sub[c] )

# Each class can learn atmost one subject in 1 period
for c in class_sub:
    for s in range(1, Session+1):
        for p in range(1, Period+1):

            model.AddAtMostOne(Schedule[(t, c, sub, p, s)] for sub in class_sub[c] for t in teacher if sub in teacher[t])

# Each class learn exactly periods of the cla-subjects
for c in class_sub:
    subject = class_sub[c]
    for sub in subject:
                        
        model.Add(sum(Schedule[(t, c, sub, p, s)] 
        for s in range(1, Session+1) for p in range(1, Period+1)
        for t in teacher if sub in teacher[t]) <= period_sub[sub])

# Each class-sub need to be teach by exactly 1 teacher
for c in class_sub:
    subject = class_sub[c]
    for sub in subject:
        for t in teacher:
            teach = model.NewBoolVar('t')
            tea = teacher[t]
            if sub in tea:
                sub_pe = sum(Schedule[(t, c, sub, p, s)] 
                for s in range(1, Session+1) for p in range(1, Period+1))

                model.Add(sub_pe == 0).OnlyEnforceIf(teach.Not())

                model.Add(sub_pe == period_sub[sub] ).OnlyEnforceIf(teach)

# The periods of the class-subject must be adjacent
for s in range(1, Session + 1):   
    for c in class_sub:
        subject = class_sub[c]
        for sub in subject:     
            pe = period_sub[sub]  
            for t in teacher:
                if sub in teacher[t]:
                    for p in range(1,Period+2-pe):
                        if p == 1:

                            model.Add(sum(Schedule[(t, c, sub, p_, s)]
                            for p_ in range(p,p+pe)) == pe).OnlyEnforceIf(Schedule[(t, c, sub, p, s)]) 

                        else:    

                            model.Add(sum(Schedule[(t, c, sub, p_, s)] 
                            for p_ in range(p,p+pe)) == pe).OnlyEnforceIf(Schedule[(t, c, sub, p, s)],Schedule[(t, c, sub, p-1, s)].Not())
                            
# Subjects must to be teached done in 1 Session
for s in range(1,Session+1):
    for c in class_sub:
        subject = class_sub[c]
        for sub in subject:
            teach = model.NewBoolVar('t')  

            sub_pe = sum(Schedule[(t, c, sub, p, s)] 
            for p in range(1, Period+1) for t in teacher if sub in teacher[t])

            model.Add( sub_pe == period_sub[sub]).OnlyEnforceIf(teach)

            model.Add(sub_pe == 0).OnlyEnforceIf(teach.Not())


# Objective function
model.Maximize(sum(Schedule[(t, c, sub, p, s)] for t in teacher for sub in teacher[t] 
for c in class_sub if sub in class_sub[c] for p in range(1,Period+1) for s in range(1,Session+1)))

# Solver
solver = cp_model.CpSolver()
status = solver.Solve(model)

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
