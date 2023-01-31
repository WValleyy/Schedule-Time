# why the copy dict modify the original one
import random as rd

# Assume that class < teacher
# Assume that studying 5 days of week, 2 sessions, 5 periods so 50 periods in week
max_pe = 50

# Create number of subjects
min_sub = 800
max_sub = 1000 #100
M = rd.randint(min_sub,max_sub)

# create subject name
Subject = [str(i) for i in range(1,M+1)]
len_sub = len(Subject)

# Create number of classes (also assume that < subject)
min_c = len_sub //2
max_c = len_sub - 1
N = rd.randint(min_c,max_c)

# Create teacher dictionary 
coef = 3 # just randomly choosing 5
T = N - rd.randint(1,coef) 

tea_dict = {i: [] for i in range(1,T+1)}

# Create an empty periods of subjects list
d = [0 for i in range(M)]

# Create dictionary with class - subject having classes
Cla = [i for i in range(1,N+1)]

Cla_sub = {i: [] for i in range(1,N+1)}


# Assign subject to class and number of periods for subject
def assign_sub():
    temp_cla = Cla[:] # for index
    temp_sub = Subject[:] # for index name
    while len(temp_sub) != 0:
        while len(temp_cla) != 0: # to assign all subject
            # assign
            rd.shuffle(temp_sub)
            name_cla = temp_cla.pop()
            name_sub = temp_sub.pop()
            Cla_sub[name_cla] += [name_sub]
        
        # the rest are random
        # assign
        name_cla = rd.choice(Cla)
        name_sub = temp_sub.pop()
        Cla_sub[name_cla] += [name_sub]

assign_sub()
# assign some random subs to class
def assign_more_subs():
    # assign some random subs to class
    for i in range(1,N+1):
        j = 0
        max_sub = 3
        ran_sub = rd.randint(1,max_sub)
        while j != ran_sub: 
            name_sub = rd.choice(Subject)
            if name_sub not in Cla_sub[i]:
                Cla_sub[i] += [name_sub]
                j += 1

assign_more_subs()

# write file part 1
f = open('data.txt','w')
f.writelines(f"{T} {N} {M}" + '\n')
# class
for i in range(1,N+1):
    f.writelines(' '.join(Cla_sub[i]) + ' 0' + '\n')


# giving period for each sub in sub_cla 
pe = {i: [] for i in range(1,N+1)} # temporary

for i in range(1,N+1):
    num_sub = len(Cla_sub[i])
    rest_pe = max_pe
    for j in range(num_sub):
        sub_pe = rd.randint(6,10)
        rest_pe -= sub_pe
        pe[i] = sub_pe


# assign a random cla-sub to teacher
tea_pe = [50 for i in range(T)]
temp_cla_sub = {key:value for key,value in Cla_sub.items()}

for i in range(1,T+1):
    ind_cla_sub = rd.choice(list(temp_cla_sub.keys()))
    if len(temp_cla_sub[ind_cla_sub]) != 0:
        name_sub = temp_cla_sub[ind_cla_sub].pop(0)
        tea_dict[i] += [name_sub]

        # add period to d
        pe_sub_cla = pe[ind_cla_sub]
        tea_pe[i-1] -= pe_sub_cla
        d[Subject.index(name_sub)] = pe_sub_cla

    # remove 0 value
    temp_cla_sub = {key:value for key,value in temp_cla_sub.items() if len(value) != 0}

# random the rest
while sum(tea_pe) != 0 and len(temp_cla_sub) != 0:
    # max left 
    tea_pe_left = [tea_pe[i] for i in range(T) if tea_pe[i] != 0]
    tea_pe_left.sort(reverse=True)
    ind_tea_pe = tea_pe.index(tea_pe_left[0])

    # random cla-sub
    ind_cla_sub = rd.choice(list(temp_cla_sub.keys()))
    if len(temp_cla_sub[ind_cla_sub]) != 0:
        rd_ind = rd.randint(0,len(temp_cla_sub[ind_cla_sub])-1)
        name_sub = temp_cla_sub[ind_cla_sub].pop(rd_ind)
        pe_sub_cla = pe[ind_cla_sub]
        if tea_pe[ind_tea_pe] >= pe_sub_cla:
            tea_dict[ind_tea_pe + 1] = list(set(tea_dict[ind_tea_pe + 1] + [name_sub])) 
            if d[Subject.index(name_sub)] == 0:
                d[Subject.index(name_sub)] += pe_sub_cla
            tea_pe[ind_tea_pe] -= pe_sub_cla
        else:
            tea_dict[ind_tea_pe + 1] = list(set(tea_dict[ind_tea_pe + 1] + [name_sub]))
            if d[Subject.index(name_sub)] == 0:
                d[Subject.index(name_sub)] += pe_sub_cla
            tea_pe[ind_tea_pe] = 0

    temp_cla_sub = {key:value for key,value in temp_cla_sub.items() if len(value) != 0}

def assign_more_subs_tea():
    # assign some random subs to teacher
    for i in range(1,T+1):
        j = 0
        max_sub = 3
        ran_sub = rd.randint(1,max_sub)
        while j != ran_sub: 
            name_sub = rd.choice(Subject)
            if name_sub not in tea_dict[i]:
                tea_dict[i] += [name_sub]
                j += 1

assign_more_subs_tea()

# write file part 2

# teacher
for j in range(1,T+1):
    f.writelines(' '.join(tea_dict[j]) + ' 0' + '\n')
# period
for k in range(M):
    f.writelines(str(d[k])+ ' ')
f.close()


