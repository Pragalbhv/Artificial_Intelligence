#!/usr/bin/env python
# coding: utf-8

# In[27]:


import random
import time


# In[3]:


# This is input stream:- genertates
D=[]
count=0
while True:
    if count ==0:
        Type=input()#sys.stdin.readline()
    elif count ==1:
        N=int(input())#sys.stdin.readline())
    elif count<=N+1:
        input()
    elif 1+N<count<=2*N+1:
        D.append(list(map(float,input().split()))) #sys.stdin.readline())))
    elif count>=2*N+2:
        break
    count=count+1
    


# In[ ]:


# 1
# 3
# 34
# 34
# 34
# 0.0 84.8383291139 84.4873344618 49.4128699795
# 84.8383291139 0.0 111.973408081
# 84.4873344618 111.973408081 0.0


# In[4]:


def closest(D, n):
    closest = []
    for i in range(n):
        dlist = [[D[i][j] ,j] for j in range(n) if j != i]#generates a list of neighbours sorted with distance from i to j
        dlist.sort()
        closest.append(dlist)
    return closest


# In[5]:


def length(tour,D,N):
    z = dist(tour[0][-1], tour[0][0],D)    # edge from last to first city of the tour
    z+=sum(tour[1])      # add length of edge from city i-1 to i
    return z


# In[6]:


def is_in(j,LIST):# checks for validity of tour by checking against duplicates
    for i in LIST:
        if j==i:
            return True
    return False


# In[7]:


def return_nearest(i,A,unvisited):#returns nearest
    j=0
    #print(len(A))
    while j < len(A):
        c=A[i][j][1]
        if is_in(c,unvisited):
            return A[i][j]
        else:
            j+=1
    return[999]
    


# In[8]:


def create_tour(D,i,N):    
    unvisited=list(range(N))
    A=closest(D,N)
    length=[]
    prev=i
    Tour=[i]
    unvisited.remove(i)
    while unvisited!=[]:
        temp=return_nearest(prev,A,unvisited)
        next=temp[1]
        length.append(temp[0])
        Tour.append(next)
        unvisited.remove(next)
        prev=next
    cost=sum(length)
    cost=cost+D[next][i]
    return (Tour,cost)


# In[9]:


def cost(Tour,D):#use only for GA created Tours with no added distance sum
    rcost=0
    lenght=len(Tour)
    for i in range(lenght-1):
        rcost=rcost+D[Tour[i]][Tour[i+1]]
        #print(rcost)
    rcost=rcost+D[Tour[lenght-1]][Tour[0]]
    return rcost


# In[10]:


def sortsol(l):
    l.sort(key = lambda x: x[1])  #sort solution wrt cost- cost is distance
    return l


# In[11]:


def fitness(sol): #calculates fitness wrt reciprocal of distance
    sum=0
    fitness_sum=0
    fitness=[]
    for i in range(len(sol)):
        fitness_sum=fitness_sum+(1/sol[i][1])**2
    for j in range(len(sol)):
        a=((1/(sol[j][1])**2)/(fitness_sum))
        fitness.append(a)
    return fitness
    


# In[12]:


def mk_parent(sol,Fitness,bestsize):
    parents=[]
    #for i in range(bestsize):
        #parents.append(sol[i][0])
    psum=0
    i=0
    for i in range(0, len(sol)): #- bestsize):
        a=random.uniform(0,1)
        psum=0
        i=0
        while True:
            psum+=Fitness[i]
            if psum>=a:
                parents.append(sol[i][0])
                break
            i+=1
    return parents


# In[13]:


def make_babies(parent1, parent2):
    child = []
    child_1 = []
    half1_1=[]
    half1_2=[]
    #child_2 = []
    #half2_1=[]
    #half2_2=[]
    
    splicepoint1 = int(random.random() * len(parent1))
    splicepoint2 = int(random.random() * len(parent1))
    
    startsplice = min(splicepoint1, splicepoint2)
    endsplice = max(splicepoint1, splicepoint2)

    for i in range(startsplice, endsplice):
        half1_1.append(parent1[i])
        #print(parent2)
        #half2_1.append(parent2[i])
        
    half1_2 = [j for j in parent2 if j not in half1_1]
    #half2_2 = [j for j in parent1 if j not in half2_1]#for legacy support in old code of mine

    child_1 = half1_1+half1_2
    #child_2 = half2_1+half2_2
    return child_1#,child_2]


# In[14]:


def babies(parents, bestsize):#creates offsprings
    children = []
    length = len(parents) - bestsize
    parentset = random.sample(parents, len(parents))

    #for i in range(0,bestsize):
        #children.append(parents[i])
    
    for i in range(0, length):
        child = make_babies(parentset[i], parentset[len(parents)-i-1])
        children.append(child)#[0])
        #children.append(child[1])
    return children


# In[15]:


def mutate(route,rate):#inversion mutation
    i=int(random.random()*len(route))
    j=int(random.random()*len(route))
    input=route[:]
    if j>i:
        route=input[:i+1]+input[j-1:i:-1] + input[j:]
    elif i>j:
        route=input[:j+1]+input[i-1:j:-1] + input[i:]
            
    return route


# In[16]:


def make_sol(tempsol):#makes the format(route,cost) as this format is beneficial
    A=[]
    costtemp=0
    for i in range(len(tempsol)):
        costtemp=cost(tempsol[i],D)
        A.append((tempsol[i],costtemp))
    return A


# In[17]:


def mutate_children(children, rate):#makes children for a range of values
    mutated=[]
    for i in range(len(children)):
        mutatedchild=mutate(children[i],rate)
        mutated.append(mutatedchild)
    return mutated


# In[18]:


def edge_exchange(route,D):#edge exchanges for two opt
    best = route
    improved = True
    while improved:
        improved = False
        for a in range(1, len(route) - 2):
            for b in range(a + 1, len(route)):
                if b - a == 1: continue  # changes nothing, skip then
                newroute = route[:]
                newroute[a:b] = route[b - 1:a - 1:-1] #this swap works for non evuclidiean as well
                if cost(newroute,D) < cost(best,D):
                    best = newroute
                    improved = True
                    route = best
    return best


# In[19]:


# def printsol(tour):
#     for i in range(len(tour)-1):
#         print(tour[i],end=' ')
#     print(tour[len(tour)-1])
#     return


# In[20]:


# def genetic_algorithmfinal(D,N,genrations,rate,bestsize=2):#the algorithm yay!
#     import random

#     sol=[]
#     solution=[]
#     #performance=[]
#     for i in range(100):
#         B=create_tour(D,i,N)
#         #T=edge_exchange(D,B)
#         #sol.append((T,cost(T,D)))
#         sol.append(B)
#     sol=sortsol(sol)
#     solution=sol[:]
#     prevbest=sol[0][0]
#     printsol(prevbest)
#     #performance.append((sol[0][1],0))
    
        
#     for i in range(genrations):
#         selected=solution[0:25]
#         R=fitness(selected)
#         parents=mk_parent(selected,fitness(selected),bestsize)
#         children=babies(parents,bestsize)
#         solset=mutate_children(children,rate)
#         solved=[]
#         for k in range(len(children)):
#             solved.append(edge_exchange(solset[k],D))
#         solution=make_sol(solved)
#         for j in range(0,bestsize):
#             solution.append(selected[j])
#         solution=sortsol(solution)
#         #print(solution)
#         best=solution[0]
#         #performance.append((best[1],i))
#         i+=1
#         if best[0]!= prevbest:
#             prevbest=best[0]
#             printsol(prevbest)
#     return
        
        


# In[29]:


# #import numpy as np#final product
# genetic_algorithmfinal(D,N,12,0.04)


# In[46]:


import time
start_time = time.time()
genrations=1000
rate=0.04
bestsize=2

sol=[]
solution=[]
#performance=[]
for i in range(N):
    B=create_tour(D,i,N)
    #T=edge_exchange(D,B)
    #sol.append((T,cost(T,D)))
    sol.append(B)
sol=sortsol(sol)
solution=sol[:]
prevbest=sol[0][0]
print(*prevbest)
#performance.append((sol[0][1],0))
elapsed_time = time.time() - start_time
time_left=290-elapsed_time
for i in range(genrations):
    if (elapsed_time>=time_left):
        break
    selected=solution[0:25]
    R=fitness(selected)
    parents=mk_parent(selected,fitness(selected),bestsize)
    children=babies(parents,bestsize)
    solset=mutate_children(children,rate)
    solved=[]
    for k in range(len(children)):
        solved.append(edge_exchange(solset[k],D))
    solution=make_sol(solved)
    for j in range(0,bestsize):
        solution.append(selected[j])
    solution=sortsol(solution)
    #print(solution)
    best=solution[0]
    #performance.append((best[1],i))
    i+=1
    if best[0]!= prevbest:
        prevbest=best[0]
        print(*prevbest)
    elapsed_time = time.time() - start_time

