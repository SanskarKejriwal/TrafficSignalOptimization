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


#particle class
class Particle:
  def __init__(self, fitness, dim, minx, maxx,seed,count):
    # random.seed(seed)
    # self.rnd = random
 
    # initialize position of the particle with 0.0 value
    self.position = [0.0 for i in range(dim)]
 
     # initialize velocity of the particle with 0.0 value
    self.velocity = [0.0 for i in range(dim)]
 
    # initialize best particle position of the particle with 0.0 value
    self.best_part_pos = [0.0 for i in range(dim)]
 
    # loop dim times to calculate random position and velocity
    # range of position and velocity is [minx, max]
    for i in range(dim):
      self.position[i] = ((maxx[i] - minx) *
        random.random() + minx)
      self.velocity[i] = ((maxx[i] - minx) *
        random.random() + minx)
 
    # compute fitness of particle
    self.fitness = fitness(self.position,count) # curr fitness
 
    # initialize best position and fitness of this particle
    self.best_part_pos = copy.copy(self.position)
    self.best_part_fitnessVal = self.fitness # best fitness

# count = [0,[1e-308]]

# particle swarm optimization function
def pso(fitness, max_iter, n, dim, minx, maxx,count,seed,w,c1,c2):
    
    count[0]=0
    count[1]=[1e308]
    count[2]=[]
    count[3]=[]
    count[4]=[]

    print("\nBeginnning PSO\n")
    print("No. of variables     = " + str(dim))
    print("No. of particles     = " + str(n))
    print("No. of iterations    = " + str(max_iter))
    print("\nStarting PSO algorithm\n")
    
    # hyper parameters
    # w = 0.729    # inertia
    # c1 = 1.5 # cognitive (particle)
    # c2 = 1.5 # social (swarm)
    
    # rnd = random
    
    # create n random particles
    swarm = []
    for i in range(n):
        swarm.append(Particle(fitness, dim, minx, maxx, seed+i,count))
    
    # for i in swarm:
    #     print(i.position)
    
    # compute the value of best_position and best_fitness in swarm
    best_swarm_pos = [0.0 for i in range(dim)]
    best_swarm_fitnessVal = 1e308 # swarm best
    
    # computer best particle of swarm and it's fitness
    for i in range(n): # check each particle
        if swarm[i].fitness < best_swarm_fitnessVal:
            best_swarm_fitnessVal = swarm[i].fitness
            best_swarm_pos = copy.copy(swarm[i].position)
    
    # main loop of pso
    Iter = 0
    while Iter < max_iter:

        avg = 0
        for i in swarm:
            avg += i.fitness
        avg /= len(swarm)
        avg = -1*avg

        #print iteration number and best fitness value so far
        print("Iter = " + str(Iter) + " best fitness = %.3f" % (-1*best_swarm_fitnessVal) + " avg fitness = %.3f" % avg)
        count[2].append(-1*best_swarm_fitnessVal)
        count[3].append(avg)
        for i in range(n): # process each particle
        
        # compute new velocity of curr particle
            for k in range(dim):
                r1 = random.random()    # randomizations
                r2 = random.random()
            
                swarm[i].velocity[k] = (
                                        (w * swarm[i].velocity[k]) +
                                        (c1 * r1 * (swarm[i].best_part_pos[k] - swarm[i].position[k])) + 
                                        (c2 * r2 * (best_swarm_pos[k]-swarm[i].position[k]))
                                    ) 
        
        
                # if velocity[k] is not in [minx, max]
                # then clip it
                if swarm[i].velocity[k] < minx:
                    swarm[i].velocity[k] = minx
                elif swarm[i].velocity[k] > maxx[k]:
                    swarm[i].velocity[k] = maxx[k]
    
         
            # compute new position using new velocity
            for k in range(dim):
                swarm[i].position[k] += swarm[i].velocity[k]
        
            # compute fitness of new position
            swarm[i].fitness = fitness(swarm[i].position,count)
        
            # is new position a new best for the particle?
            if swarm[i].fitness < swarm[i].best_part_fitnessVal:
                swarm[i].best_part_fitnessVal = swarm[i].fitness
                swarm[i].best_part_pos = copy.copy(swarm[i].position)
        
            # is new position a new best overall?
            if swarm[i].fitness < best_swarm_fitnessVal:
                best_swarm_fitnessVal = swarm[i].fitness
                best_swarm_pos = copy.copy(swarm[i].position)
        
            # for-each particle

        Iter += 1
    #end_while

    print("\nPSO completed\n")
    print("\nBest solution found:")
    # print(["%.6f"%best_swarm_pos[k] for k in range(dim)])
    print("fitness of best solution = %.6f" % (-1*best_swarm_fitnessVal))
    print("Count of function computations = %.6f" % count[0])

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
max_iter = 100

parser = argparse.ArgumentParser()
parser.add_argument("-c", '--count')

max_iter = 300
w = [0.4, 0.9]
c1 = [1.5,1.6,1.7,1.8,1.9]
c2 = [1.5,1.6,1.7,1.8,1.9]

i = int(parser.parse_args().count)

pso(fitness, max_iter, num_particles, dim, minn, maxx, count,100,w[i%2],c1[i],c2[i])
with open('./pso/run'+str(i)+'.csv', 'w') as file_writer:
    
    help(file_writer)