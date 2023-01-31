from queue import PriorityQueue
import time
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

period_sub.insert(0,0)
#print(class_sub)
#print(teacher)
#print(period_sub)

#Construct list of candidates:
candidates = []
for c in class_sub:
    for sub in class_sub[c]:
        p = period_sub[sub]
        for i in range(p):
            candidates.append((sub,c)) #containing subject-class tuples

#print(candidates)


def select(t,mark):
    for y in candidates:
        if (y[0] in teacher[t]) and (mark[y[1]] == False):
            return y
    #print('cant select s-c for teacher',t,candidates)
    return None

def simpleGreedy():
    global candidates
    S = []
    count = 1 # 1<=count<=50 : 
    while (len(candidates) > 0):
        mark = [False for c in range(N+1)] # mark classes that have already scheduled (in current iteration)
        temp = []
        for t in teacher:
            x = select(t,mark)
            if x == None:
                S.append((count,t,None))
                continue
            candidates.remove(x)
            S.append((count,t,x))
            mark[x[1]] = True
        #print(mark[1:])
        count+=1
    print(count)
    return S

def improvedGreedy():
    global candidates
    S = []
    teacher_queue = PriorityQueue()
    for t in teacher:
        teacher_queue.put((0,t))
    count = 1 # 1<=count<=50 : 
    while (len(candidates) > 0):
        mark = [False for c in range(N+1)] # mark classes that have already scheduled (in current iteration)
        temp = []
        while not teacher_queue.empty():
            t = teacher_queue.get()
            x = select(t[1],mark)
            if x == None:
                S.append((count,t[1],None))
                temp.append((t[0],t[1]))
                continue
            candidates.remove(x)
            S.append((count,t[1],x))
            temp.append((t[0]+1,t[1]))
            mark[x[1]] = True
        #print(mark[1:])
        for t in temp:
            teacher_queue.put(t)
        count+=1
    print('teaching stop at period ',count-1)
    print('-'*70)
    return S
start_time = time.time()
S = improvedGreedy()
end_time = time.time()
count = 0
pe = 0
for i in S:
    if i[2] != None:
        count += 1
        
        session = i[0] // 5 + 1
        if i[0] % 5 == 0:
            session = i[0] // 5
        if i[0] - (session - 1)*5 < pe:
            print('-'*70)
        pe = i[0] - (session - 1)*5
        print('teacher ',i[1],'teach class ',i[2][1],' the subject ',i[2][0], ' at period ',pe,' in session ',session )
        

print('-'*70)
print('teachers have teaching total ',count, ' periods')
elapsed_time = end_time - start_time
print('-'*70)
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
    

