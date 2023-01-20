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

'''
print(class_sub)
print(teacher_sub)
print(period_sub)
'''

# Modelling

model = cp_model.CpModel()
Period = 5
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

'''
# Teacher can teach max 5 period in a session : dont need because we create the constraint below
for t in teacher:
    for s in range(1, Session+1):
        model.Add(sum(Schedule[(t, c, sub, p, s)] for c in class_teacher_can_teach[t]
        for p in range(1, Period+1) for sub in teacher[t]) <= Period)
'''

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

# Each class learn full of period of the subjects
for c in class_sub:
    subject = class_sub[c]
    for sub in subject:                
        model.Add(sum(Schedule[(t, c, sub, p, s)] 
        for s in range(1, Session+1) for p in range(1, Period+1)
        for t in teacher if sub in teacher[t]) == period_sub[sub-1])

# Each class-sub need to be teach by exactly 1 teacher
for c in class_sub:
    subject = class_sub[c]
    for sub in subject:
        for t in teacher:
            teach = model.NewBoolVar('t')
            if sub in teacher[t]:
                model.Add(sum(Schedule[(t, c, sub, p, s)] 
                for s in range(1, Session+1) for p in range(1, Period+1)) == 0).OnlyEnforceIf(teach.Not())
                model.Add(sum(Schedule[(t, c, sub, p, s)] 
                for s in range(1, Session+1) for p in range(1, Period+1)) == period_sub[sub-1] ).OnlyEnforceIf(teach)

solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0
solver.parameters.enumerate_all_solutions = True

#Solution Printer
class SolutionPrinterClass(cp_model.CpSolverSolutionCallback):
    def __init__(self, Schedule, teacher, class_sub, Session, Period,limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.Schedule = Schedule
        self.teacher = teacher
        self.class_sub = class_sub
        self.Session = Session
        self.Period = Period
        self.solution_count = 0
        self.solution_limit = limit
    def on_solution_callback(self):
            self.solution_count += 1
            print('Solution %i' % self.solution_count)
            for s in range(1, self.Session+1):
                print('Session ' + str(s))
                for t in self.teacher:
                    
                    for c in self.class_sub:
                        
                        for sub in self.teacher[t]:
                
                            for p in range(1, self.Period + 1):
                        
                    
                                if self.Value(self.Schedule[(t, c, sub, p, s)]):
                                    
                                    print('Teacher ' + str(t) + ' teach class ' +
                                          str(c) + ' the subject ' + str(sub) + ' at period ' + str(p))
                                    

            
            if self.solution_count >= self.solution_limit:
                print('Stop search after %i solutions' % self.solution_count)
                self.StopSearch()
            

    def _solution_count(self):
        return self.solution_count

solution_limit = 1
solution_printer = SolutionPrinterClass(Schedule, teacher, class_sub, Session, Period,solution_limit)
solver.Solve(model,solution_printer)

# Statistics.
print('\nStatistics')
print('  - conflicts      : %i' % solver.NumConflicts())
print('  - branches       : %i' % solver.NumBranches())
print('  - wall time      : %f s' % solver.WallTime())
print('  - solutions found: %i' % solution_printer._solution_count())

'''

# Solver
solver = cp_model.CpSolver()
status = solver.Solve(model)
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    for s in range(1, Session+1):
                print('Session ' + str(s))
                for t in teacher:
                    
                    for c in class_sub:
                        
                        for sub in teacher[t]:
                
                            for p in range(1, Period + 1):
                        
                    
                                if solver.Value(Schedule[(t, c, sub, p, s)]):
                                    
                                    print('Teacher ' + str(t) + ' teach class ' +
                                          str(c) + ' the subject ' + str(sub) + ' at period ' + str(p))
                                    
                    
    print()
else:
    print('No solution found.')
'''


'''
3 3 8
1 2 3 4 5 6 7 8 0
1 2 3 4 5 6 7 8 0
1 2 3 4 5 6 7 8 0
1 5 0
2 3 4 0
6 7 8 0
2 3 2 2 3 2 2 8
'''
