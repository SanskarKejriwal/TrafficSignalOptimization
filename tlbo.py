import random
from collections import deque
import copy
import csv
import argparse

fileObject = open("e.txt","r")
# random.seed(10)

class car:
    key = int()
    strt = str()
    enterTime = int()
    endTime = 1e9
    now = 0
    def __init__(self,key):
        self.key = key

class street:
    B,E,L = (int,)*3 
    name = str()
    q = deque()
    def __init__(self,B,E,L,name):
        self.B = B
        self.E = E
        self.L = L
        self.name = name
        self.q = deque()

class intersection:
    key = int()
    incom = []
    schd = []
    def __init__(self,key):
        self.key = key
        self.incom = []
        self.schd = []

def inp():
    D,I,S,V,F = [int(x) for x in fileObject.readline().split()]

    for i in range(I):
        inscn.append(intersection(i))

    for i in range(S):

        B,E,name,L = fileObject.readline().split()
        B=int(B)
        E=int(E)
        L=int(L)

        strt = street(B,E,L,name)
        um[name] = strt
        inscn[E].incom.append(strt)
        st.append(strt)
    
    for i in range(V):
        x = fileObject.readline().split()
        
        cr = car(i)

        path[cr] = []
        c.append(cr)

        pth = int(x[0])
        for j in range(pth):
            name = x[j+1]
            path[cr].append(um[name])
            if j == 0 :
                um[name].q.append(cr)
                cr.enterTime = -1*(um[name].L)
                cr.strt = name

    maxx = []
    for i in inscn:
        for j in range(D):
            maxx.append(len(i.incom))

    return [D,I,S,V,F,maxx]


D,I,S,V,F = (int(),)*5
maxx = []
st = []
c = []
inscn = []
path = {}
um = {}
count = [0,[1e308],[],[],[]]

D,I,S,V,F,maxx = inp()

redundant = street(-1,-1,-1,"red")

def schedule(population,count):

    for i in range(I*D):

        x = population[i]
        x = int(x)

        ind = int(i/D)
        y = int(i%D)

        if x >= len(inscn[ind].incom) :
            if count[0]==0:
                inscn[ind].schd.append(redundant)
            else :
                inscn[ind].schd[y] = redundant

        else :
            if count[0]==0:
                inscn[ind].schd.append(inscn[ind].incom[x])
            else :
                inscn[ind].schd[y] = inscn[ind].incom[x]

    penalty = 0

    for i in range(I):

        mp = {}
        
        for j in range(S):
            mp[st[j].name]=0

        mp[inscn[i].schd[0].name]=1

        for j in range(1,D):
            strt = inscn[i].schd[j].name
            prevstrt = inscn[i].schd[j-1].name
            if strt == 'red' or strt == prevstrt:
                continue
            mp[strt] = mp[strt]+1
        
        for j in range(S):
            x = mp[st[j].name]
            if x>1: 
               penalty += (x-1)*1e10


    return penalty 

def traffic():
    
    for t in range(D):

        for i in range(I):

            strt = inscn[i].schd[t]

            if strt.B==-1:
                continue

            if len(strt.q) > 0:

                cr1 = strt.q[0]

                if t - cr1.enterTime >= strt.L :
                    
                    cr = strt.q.popleft()

                    cr.now = cr.now + 1

                    temp_str = path[cr][cr.now]
                    endTime = t + path[cr][-1].L 

                    if temp_str.name == path[cr][-1].name and endTime <= D :
                        cr.endTime = endTime
                    else :
                        path[cr][cr.now].q.append(cr)
                        cr.strt = path[cr][cr.now].name
                        cr.enterTime = t

def objective():
    obj = 0

    for i in range(V):
        if c[i].endTime != 1e9 :
            obj = obj + F + (D-c[i].endTime)
    
    return obj

# fitness function
def fitness(population,count):
    objective_value = schedule(population,count)
    traffic()
    h = objective()
    # print(h, "--------------------------------------------------")
    count[0]=count[0]+1
    objective_value -= h
    # print(objective_value)    
    count[1].append(min(objective_value,count[1][-1]))
    count[4].append(objective_value)
    return objective_value

#Student class
class Student:
  def __init__(self, fitness, dim, minx, maxx, seed,count):
    # random.seed(seed)
    # self.random = random
 
    # a list of size dim
    # with 0.0 as value of all the elements
    self.position = [0.0 for i in range(dim)]
 
    # loop dim times and randomly select value of decision var
    # value should be in between minx and maxx
    for i in range(dim):
      self.position[i] = ((maxx[i] - minx)*random.random() + minx)
    #   self.position[i] = int(self.position[i]) #added!!
 
    # compute the fitness of student
    self.fitness = fitness(self.position,count)
 
# count = [0,[1e308]]

    # Teaching learning based optimization
def tlbo(fitness, max_iter, n, dim, minx, maxx,count,seed):
    
    count[0]=0
    count[1]=[1e308]
    count[2]=[]
    count[3]=[]
    count[4]=[]

    print("\nBeginnning TLBO\n")
    print("No. of variables     = " + str(dim))
    print("No. of particles     = " + str(n))
    print("No. of iterations    = " + str(max_iter))
    print("\nStarting TLBO algorithm\n")
    
    # create n random students
    classroom = []
    for i in range(n):
        classroom.append(Student(fitness, dim, minx, maxx, seed+i,count))
    
    # for i in classroom:
    #     print(i.position)
    
    # compute the value of best_position and best_fitness in the classroom
    Xbest = [0.0 for i in range(dim)]
    Fbest = 1e308       
    
    for i in range(n): # check each Student
        if classroom[i].fitness < Fbest:
            Fbest = classroom[i].fitness
            Xbest = copy.copy(classroom[i].position)
    
    # main loop of tlbo
    Iter = 0
    while Iter < max_iter:

        avg = 0
        for i in classroom:
            avg += i.fitness
        avg /= n
        avg = -1*avg

        print("Iter = " + str(Iter) + " best fitness = %.3f " % (-1*Fbest) + "avg fitness = %.3f" % avg)
        count[2].append(-1*Fbest)
        count[3].append(avg)
        # for each student of classroom
        for i in range(n):
    
        ### Teaching phase of ith student
    
            # compute the mean of all the students in the class
            Xmean = [0.0 for i in range(dim)]
            for k in range(n):
                for j in range(dim):
                    Xmean[j]+= classroom[k].position[j]
                
            for j in range(dim):
                Xmean[j]/= n;
            
        
            # teaching factor (TF)
            # either 1 or 2 ( randomly chosen)
            TF = random.randint(1, 2)
        
            # best student of the class is teacher
            Xteacher = Xbest
        
            # initialize new solution
            Xnew = [0.0 for i in range(dim)]
            
            # compute new solution
            for j in range(dim):
                lm = random.random()*(Xteacher[j] - TF*Xmean[j])
                Xnew[j] = classroom[i].position[j] + lm
                # Xnew[j] = int(Xnew[j]) #added
                # print(lm, Xnew[j])
            
            # if Xnew < minx OR Xnew > maxx
            # then clip it
            for j in range(dim):
                if Xnew[j] < minx:
                    Xnew[j] = minx
                if Xnew[j] > maxx[j]:
                    Xnew[j] = maxx[j]
            
            # compute fitness of new solution
            fnew = fitness(Xnew,count)
        
            # if new solution is better than old
            # replace old with new solution
            if(fnew < classroom[i].fitness):
                classroom[i].position = Xnew
                classroom[i].fitness = fnew
                
            # update best student
            if(fnew < Fbest):
                Fbest = fnew
                Xbest = Xnew
        
            ### learning phase of ith student
        
            # randomly choose a solution from classroom
            # chosen solution should not be ith student
            p = random.randint(0, n-1)
            while(p==i):
                p = random.randint(0, n-1)
            
            # partner solution
            Xpartner = classroom[p]
        
            Xnew = [0.0 for i in range(dim)]
            if(classroom[i].fitness < Xpartner.fitness):
                for j in range(dim):
                    Xnew[j] = classroom[i].position[j] + random.random()*(classroom[i].position[j] - Xpartner.position[j])
            else:
                for j in range(dim):
                    Xnew[j] = classroom[i].position[j] - random.random()*(classroom[i].position[j] - Xpartner.position[j])
        
            # if Xnew < minx OR Xnew > maxx
            # then clip it
            for j in range(dim):
                # Xnew[j] = abs(Xnew[j])
                # if Xnew[j] < minx:
                #     Xnew[j] = abs(Xnew[j])
                # if Xnew[j] > maxx[j]:
                #     Xnew[j] = Xnew[j] - (int(Xnew[j])/int(maxx[j]))*maxx[j]
                
                Xnew[j] = max(Xnew[j], minx)
                Xnew[j] = min(Xnew[j], maxx[j])
            
            # compute fitness of new solution
            fnew = fitness(Xnew,count)
        
            # if new solution is better than old
            # replace old with new solution
            if(fnew < classroom[i].fitness):
                classroom[i].position = Xnew
                classroom[i].fitness = fnew
                
            # update best student
            if(fnew < Fbest):
                Fbest = fnew
                Xbest = Xnew

            # print(Xbest)
    
        Iter += 1
    # end-while
    
    best_pos = Xbest

    print("\nTLBO completed\n")
    print("\nBest solution found:")
    # print(["%.6f"%best_pos[k] for k in range(dim)])
    print("fitness of best solution = %.6f" % (-1*Fbest))
    print("Count of function computations = %.6f" % count[0])

    # return best student from classroom
    # end pso
 
 
#----------------------------
# Driver code for rastrigin function

def help(file_writer):

    data_header = ['Functional Evaluations', 'Best Fitness', 'Avg Fitness','Function Evaluations']
    
    writer = csv.writer(file_writer)

    writer.writerow(data_header[0])
    for i in range(len(count[1])):
        count[1][i] = -1*count[1][i]
    writer.writerow(count[1])
    writer.writerow(data_header[1])
    writer.writerow(count[2])
    writer.writerow(data_header[2])
    writer.writerow(count[3])
    writer.writerow(data_header[3])
    for i in range(len(count[4])):
        count[4][i] = -1*count[4][i]
    writer.writerow(count[4])


minn = 0
dim = I*D
num_particles = 15

max_iter = 120

parser = argparse.ArgumentParser()
parser.add_argument("-c", '--count')

i = int(parser.parse_args().count)

tlbo(fitness, max_iter, num_particles, dim, minn, maxx,count,100)

with open('./tlbo/run'+str(i)+'.csv', 'w') as file_writer:
        
    help(file_writer)