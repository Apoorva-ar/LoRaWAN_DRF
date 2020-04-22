from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import sys
import simpy
import numpy as np
import Uplink
import Downlink
import coordinates
import classes
import random


ADR=1
pingDelay=0
beaconDelay=0
pingsSent=0
switchBack=0
# this is an array with measured values for sensitivity
bandwidth = np.array([0,125,250,500])
sf7 = np.array([7,-126.5,-124.25,-120.75])
sf8 = np.array([8,-127.25,-126.75,-124.0])
sf9 = np.array([9,-131.25,-128.25,-127.5])
sf10 = np.array([10,-132.75,-130.25,-128.75])
sf11 = np.array([11,-134.5,-132.75,-128.75])
sf12 = np.array([12,-133.25,-132.25,-132.25])
sensi =np.array([bandwidth,sf7,sf8,sf9,sf10,sf11,sf12])

#p=[0.8,0.8,0.8,0.8,0.8,0.8,0.8]
#p=[0.1,0.1,0.1,0.1,0.1,0.1,0.1]
p=[0.2,0.2,0.2,0.2,0.2,0.2,0.2]
#p=[0.7,0.7,0.7,0.7,0.7,0.7,0.7]
#p=[0.5,0.5,0.5,0.5,0.5,0.5,0.5]
#p=[0.4,0.4,0.4,0.4,0.4,0.4,0.4]
#p=[1,1,1,1,1,1,1]
#p=[0,0,0,0,0,0,0]
nrNodes = 20
simtime = 30000000

# turn on/off graphics
graphics = 1
R3=24000
if (graphics == 1):
    plt.ion()
    plt.figure()
    ax = plt.gcf().gca()
    rectangle = plt.Rectangle((-R3, -R3), 20*R3, 20*R3, fc='blue',alpha=0.6)
    ax.add_patch(rectangle)
    plt.xlim([-R3, R3])
    plt.ylim([-R3, R3])
    plt.draw()
    plt.show()

#global
bs=[]
packetsAtBS=[]
nodes=[]
beaconCount=0
LRCIndex=0
id=[[],[],[],[],[],[],[]]


nrBS=60   
nrBS1=6
nrBS2=7
nrBS3=15
nrBS4=7
nrBS5=10
nrBS6=5
nrBS7=10

r1= 7500
xo1= 8000
yo1 = 8000

xo2 = -5000
yo2 = 2000

xo3= 5000
yo3 = -12000

xo4= 17000
yo4 = -9000

xo5= -10000
yo5 = -12000

xo6= -17000
yo6 = 4000

xo7= -12000
yo7 = 15000

circ1 = plt.Circle((xo1, yo1), r1, color='w', alpha=0.8)
plt.text(xo1, yo1, 1, fontsize=20)
circ2 = plt.Circle((xo2, yo2), r1-500, color='w', alpha=0.8)
plt.text(xo2, yo2, 2, fontsize=20)
circ3 = plt.Circle((xo3, yo3), r1-700, color='w', alpha=0.8)
plt.text(xo3, yo3, 3, fontsize=20)
circ4 = plt.Circle((xo4, yo4), r1-800, color='w', alpha=0.8)
plt.text(xo4, yo4, 4, fontsize=20)
circ5 = plt.Circle((xo5, yo5), r1-800, color='w', alpha=0.8)
plt.text(xo5, yo5, 5, fontsize=20)
circ6 = plt.Circle((xo6, yo6), r1+1000, color='w', alpha=0.8)
plt.text(xo6, yo6, 6, fontsize=20)
circ7 = plt.Circle((xo7, yo7), r1+1000, color='w', alpha=0.8)
plt.text(xo7, yo7, 7, fontsize=20)

# ax.add_patch(circ1)
# ax.add_patch(circ2)

# ax.add_patch(circ3)
# ax.add_patch(circ4)
# ax.add_patch(circ5)
# ax.add_patch(circ6)
# ax.add_patch(circ7)




env = simpy.Environment()
env.process(Downlink.LRCbeaconIndex(env))


for i in range(0,nrBS1): #21
    x, y = coordinates.cordinatesgws[i]
    plt.text(x, y, i, fontsize=12)
    circ = plt.Circle((x, y), 500, color='green', alpha=0.3)
    ax.add_patch(circ)

    b = classes.myBS(i,x,y)
    id[0].append(i)
    if(not(ADR)):
        env.process(Downlink.BeaconProcess(env,b,p[0],env.now,1)) 
    bs.append(b)
    packetsAtBS.append([]) #append an empty array specific to bs created
  

for i in range(0,nrBS2): #25
    x, y = coordinates.cordinatesgws[i+nrBS1]
    plt.text(x, y, i+nrBS1, fontsize=12)
    circ = plt.Circle((x, y), 500, color='green', alpha=0.3)
    ax.add_patch(circ)
    
    b = classes.myBS(i+nrBS1,x,y)
    id[1].append(i+nrBS1)
    if(not(ADR)):
        env.process(Downlink.BeaconProcess(env,b,p[1],env.now,1)) 
    bs.append(b)
    packetsAtBS.append([])

for i in range(0,nrBS3): #15
    x, y = coordinates.cordinatesgws[i+nrBS1+nrBS2]
    
    plt.text(x, y, i+nrBS1+nrBS2, fontsize=12)
   
    circ = plt.Circle((x, y), 500, color='green', alpha=0.3)
    ax.add_patch(circ)
    

    b = classes.myBS(i+nrBS1+nrBS2,x,y)
    id[2].append(i+nrBS1+nrBS2)
    if(not(ADR)):
      env.process(Downlink.BeaconProcess(env,b,p[2],env.now,1)) 
    bs.append(b)
    packetsAtBS.append([])
    
for i in range(0,nrBS4): #25
    x, y = coordinates.cordinatesgws[i+nrBS1+nrBS2+nrBS3]
    plt.text(x, y, i+nrBS1+nrBS2+nrBS3, fontsize=12)
    circ = plt.Circle((x, y), 500, color='green', alpha=0.3)
    ax.add_patch(circ)
    
    b = classes.myBS(i+nrBS1+nrBS2+nrBS3,x,y)
    id[3].append(i+nrBS1+nrBS2+nrBS3)
    if(not(ADR)):
        env.process(Downlink.BeaconProcess(env,b,p[3],env.now,1)) 
    bs.append(b)
    packetsAtBS.append([])


for i in range(0,nrBS5): #25
    x, y = coordinates.cordinatesgws[i+nrBS1+nrBS2+nrBS3+nrBS4]
    plt.text(x, y,i+nrBS1+nrBS2+nrBS3+nrBS4, fontsize=12)
    circ = plt.Circle((x, y), 500, color='green', alpha=0.3)
    ax.add_patch(circ)
    
    b = classes.myBS(i+nrBS1+nrBS2+nrBS3+nrBS4,x,y)
    id[4].append(i+nrBS1+nrBS2+nrBS3+nrBS4)
    if(not(ADR)):
        env.process(Downlink.BeaconProcess(env,b,p[4],env.now,1)) 
    bs.append(b)
    packetsAtBS.append([])

for i in range(0,nrBS6): #25
    x, y = coordinates.cordinatesgws[i+nrBS1+nrBS2+nrBS3+nrBS4+nrBS5]
    plt.text(x, y, i+nrBS1+nrBS2+nrBS3+nrBS4+nrBS5, fontsize=12)
    circ = plt.Circle((x, y), 500, color='green', alpha=0.3)
    ax.add_patch(circ)
    
    b = classes.myBS(i+nrBS1+nrBS2+nrBS3+nrBS4+nrBS5,x,y)
    id[5].append(i+nrBS1+nrBS2+nrBS3+nrBS4+nrBS5)
    if(not(ADR)):
       env.process(Downlink.BeaconProcess(env,b,p[5],env.now,1)) 
    bs.append(b)
    packetsAtBS.append([])
 
for i in range(0,nrBS7): #25
    x, y = coordinates.cordinatesgws[i+nrBS1+nrBS2+nrBS3+nrBS4+nrBS5+nrBS6]
    plt.text(x, y, i+nrBS1+nrBS2+nrBS3+nrBS4+nrBS5+nrBS6, fontsize=12)
    circ = plt.Circle((x, y), 500, color='green', alpha=0.3)
    ax.add_patch(circ)
    
    b = classes.myBS(i+nrBS1+nrBS2+nrBS3+nrBS4+nrBS5+nrBS6,x,y)
    id[6].append(i+nrBS1+nrBS2+nrBS3+nrBS4+nrBS5+nrBS6)
    if(not(ADR)):
        env.process(Downlink.BeaconProcess(env,b,p[6],env.now,1)) 
    bs.append(b)
    packetsAtBS.append([])


for i in range(0,nrNodes):
    posx,posy=coordinates.coordED_100[i] 
    plt.text(posx, posy, i, color='r', fontsize=12)
   
    circ = plt.Circle((posx, posy), 500, color='red', alpha=0.3,)
    ax.add_patch(circ)
    
    
    period=100000+random.randint(10000,100000)
    node = classes.myNode(i, period,posx,posy) 
    nodes.append(node)
    #node.pingProb=random.random()
    env.process(Uplink.Ack(env,node))
    
    env.process(Downlink.CheckBeaconCol(env,node))

activatedSet=[]
subsets=[]
universe = set(range(0, nrNodes))
gwED=[[] for _ in range(0,nrBS)]
cover2=[]
threshold= 10

#----------------------------------
def set_cover(universe, subsets):
    """Find a family of subsets that covers the universal set"""
    elements = set(e for s in subsets for e in s)
    # Check the subsets cover the universe
    if elements != universe:
        return None
    covered = set()
    cover = []
    # Greedily add the subsets with the most uncovered points
    while covered != elements:
        subset = max(subsets, key=lambda s: len(s - covered))
        cover.append(subset)
        
        covered |= subset
 
    return cover

def create_subsets():
    for node1 in nodes:
        for gwnum in node1.receivingGws2: 
            
            gwED[gwnum].append(node1.id) #gwED[gwnum] is one set
            
    for gw in range(0,nrBS) :
        subsets.append(set(gwED[gw])) # list of sets
    return subsets



def greedy(env):
    
    yield env.timeout(128000*10)
    subsets=create_subsets()
    cover= set_cover(universe,subsets)
    
    
    for s in subsets:
        for c in cover:
            if(s.intersection(c)==c):
                activatedSet.append(subsets.index(s))
                env.process(Downlink.BeaconProcess(env,bs[subsets.index(s)],random.randint(5,10)/10,env.now,1))
                subsets.pop(subsets.index(s))
                cover.pop(cover.index(c))
    # for s in subsets:
    #     print(len(s))
   
    



if ADR:
    env.process(greedy(env))

if(ADR):
    simtime=simtime+128000*10

env.run(until=simtime)
# subsets=create_subsets()

# cover= set_cover(universe,subsets)
# print(cover)


#--------------------------------------------------

       





