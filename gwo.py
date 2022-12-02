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

#fitness, max_iter, num_particles, dim, minn, maxx

# wolf class
class wolf:
  def __init__(self, fitness, dim, minx,maxx,seed,count):
    # random.seed(seed)
    # self.random = random
    self.position = [0.0 for i in range(dim)]
 
    for i in range(dim):
      self.position[i] = ((maxx[i] - minx) * random.random() + minx)
 
    self.fitness = fitness(self.position,count) # curr fitness
 
# grey wolf optimization (GWO)
def gwo(fitness, max_iter, n, dim, minx, maxx, count,seed):

    count[0]=0
    count[1]=[1e308]
    count[2]=[]
    count[3]=[]
    count[4]=[]

    print("\nBeginnning GWO\n")
    print("No. of variables     = " + str(dim))
    print("No. of particles     = " + str(n))
    print("No. of iterations    = " + str(max_iter))
    print("\nStarting GWO algorithm\n")

 
    # create n random wolves
    population = []
    for i in range(n):
        population.append(wolf(fitness, dim, minx, maxx, seed+i, count))
    
    # for i in population:
    #     print(i.position)
 
    # On the basis of fitness values of wolves
    # sort the population in asc order
    population = sorted(population, key = lambda temp: temp.fitness)
 
    # best 3 solutions will be called as
    # alpha, beta and gaama
    alpha_wolf, beta_wolf, gamma_wolf = copy.copy(population[: 3])
    # main loop of gwo
    Iter = 0

    while Iter < max_iter:
        
        avg = 0
        for i in population:
            avg += i.fitness
        avg /= len(population)
        avg = -1*avg

        # after every 10 iterations
        # print iteration number and best fitness value so far
        print("Iter = " + str(Iter) + " best fitness = %.3f " % (-1*alpha_wolf.fitness) + "avg fittness = %.3f" % avg)
        count[2].append(-1*alpha_wolf.fitness)
        count[3].append(avg)

        # linearly decreased from 2 to 0
        a = 2*(1 - Iter/max_iter)
 
        # updating each population member with the help of best three members
        for i in range(n):
            A1, A2, A3 = a * (2 * random.random() - 1), a * (
              2 * random.random() - 1), a * (2 * random.random() - 1)
            C1, C2, C3 = 2 * random.random(), 2*random.random(), 2*random.random()
 
            X1 = [0.0 for i in range(dim)]
            X2 = [0.0 for i in range(dim)]
            X3 = [0.0 for i in range(dim)]
            Xnew = [0.0 for i in range(dim)]
            for j in range(dim):
                X1[j] = alpha_wolf.position[j] - A1 * abs(
                  C1 * alpha_wolf.position[j] - population[i].position[j])
                X2[j] = beta_wolf.position[j] - A2 * abs(
                  C2 *  beta_wolf.position[j] - population[i].position[j])
                X3[j] = gamma_wolf.position[j] - A3 * abs(
                  C3 * gamma_wolf.position[j] - population[i].position[j])
                Xnew[j] += X1[j] + X2[j] + X3[j]
             
            for j in range(dim):
                Xnew[j]/=3.0
                if Xnew[j] < minx:
                    Xnew[j] = minx
                if Xnew[j] > maxx[j]:
                    Xnew[j] = maxx[j]
             
            # fitness calculation of new solution
            fnew = fitness(Xnew,count)
 
            # greedy selection
            if fnew < population[i].fitness:
                population[i].position = Xnew
                population[i].fitness = fnew
                 
        # On the basis of fitness values of wolves
        # sort the population in asc order
        population = sorted(population, key = lambda temp: temp.fitness)
 
        # best 3 solutions will be called as
        # alpha, beta and gaama
        alpha_wolf, beta_wolf, gamma_wolf = copy.copy(population[: 3])
         
        Iter+= 1
    # end-while    

    best_position = alpha_wolf.position
    print("\nGWO completed\n")
    print("\nBest solution found:")
    # print(["%.6f"%best_position[k] for k in range(dim)])
    print("fitness of best solution = %.6f" % (-1*alpha_wolf.fitness))
    print("Count of function computations: %.6f" % count[0])
    # returning the best solution
    # print(globals())
           
#----------------------------
 
#Driver code for rastrigin function

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

max_iter = 70

parser = argparse.ArgumentParser()
parser.add_argument("-c", '--count')


i = int(parser.parse_args().count)

gwo(fitness, max_iter, num_particles, dim, minn, maxx,count,100)

with open('./gwo/run'+str(i)+'.csv', 'w') as file_writer:
        
    help(file_writer)
