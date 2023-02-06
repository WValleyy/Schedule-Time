from queue import PriorityQueue
import sys
# Create input
teacher= {}
class_sub = {}
period_sub = {}
[T, N, M] = [int(x) for x in sys.stdin.readline().split()] # number of teacher,class,subject
for i in range(1, N+1):
        class_sub[i] ={int(x) for x in sys.stdin.readline().split()[:-1]}
for j in range(N+1, T+N+1):
        teacher[j-N] = {int(x) for x in sys.stdin.readline().split()[:-1]}
period_sub = [int(x) for x in sys.stdin.readline().split()]


period_sub.insert(0,0)

#Construct list of C and priority
C = []
mark = [[0 for sessons in range(11)] for room in range(N+1)]
for c in class_sub:
    for sub in class_sub[c]:
        p = period_sub[sub]
        C.append((sub,c,p)) #containing subject-class tuples
        
C= sorted(C, key = lambda x: x[2] and x[1] ,reverse=True)
print(C)
teacher_queue = PriorityQueue()
for t in teacher:
    teacher_queue.put((0,t,[0 for sessons in range(11)]))

# provide continuous classes for teacher and classes that sastify the conditions
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
# provide classes for teacher and classes that satisfy the conditions
def select2(name_teacher,classes_teacher):
    global C
    for y in C:

        if (y[0] in teacher[name_teacher]):
            for i in range(1,11):
                 if (mark[y[1]][i]+y[2]<=6) and (classes_teacher[i]+y[2]<=6) :
                    if mark[y[1]][i] >= classes_teacher[i]:
                        classes_teacher[i] = mark[y[1]][i]+y[2]
                        mark[y[1]][i] = mark[y[1]][i]+y[2]
                    else:
                        mark[y[1]][i] = classes_teacher[i]+y[2]
                        classes_teacher[i] = classes_teacher[i]+y[2]
                    return y,(mark[y[1]][i]-y[2]+1,i),classes_teacher  
                
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

def improvedGreedy():
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
            x,s,c_t = select2(t[1],t[2])

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
            return S
        for t in temp:
            teacher_queue.put(t) 
     
    return S

S1 = Greedy()
S2 = improvedGreedy()
S=[]

S=S1+S2
S.sort()
print('----------------------------------------------------------------')
print(len(S))
with open('data.txt','w') as f:
    
    f.write(str(len(S))+'\n')
    for i in S:
        for v in i:
            f.write(str(v)+" ")
        f.write('\n')
    f.close()
'''
37
1 3 1 1
1 4 7 2
1 9 13 4
1 10 5 4
2 1 5 1
2 5 7 1
2 10 1 4
3 8 2 3
3 9 7 4
4 3 13 1
4 4 2 2
4 6 7...

    '''
