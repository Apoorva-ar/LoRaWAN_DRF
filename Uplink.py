import simpy
import random
import numpy as np
import math
import sys
from operator import itemgetter
import classes
import main

nrBS=60
AckOnairTime = 827.39 # explicit header, CRC enabled, payload=3, cr=1, sf=12, bw=125
maxPrea= 2**12/(1.0*125) * (8 - 5)



def Ack(env,node): # an instance for each node 
    while(True):
      ans=-1
      node.retFlag=-1
      if(node.nfcount-node.fcount!=1 and node.retcount<7): # mismatch in fcount when a confirmed frame is not acknowledged
          node.retFlag=1
          
          yield env.timeout(random.expovariate(1.0/node.period))
          AckFlag = yield env.process(transmit(env,node,-1,node.retFlag)) # 1 for retransmission and 0 for new frame
          
          
      else: 
          # no mismatch or ret attempts exceed 7; then a new frame is sent
          if(node.retcount>=7):
              node.retcount=0
              node.nfcount=node.fcount+1
          node.retFlag=0
          yield env.timeout(random.expovariate(1.0/float(node.period)))
          AckFlag = yield env.process(transmit(env,node,-1,node.retFlag)) 
      #print("AckFlag",AckFlag)
      if(AckFlag==1):  #sets ans to 1 or 0
        
        tx=node.txArr[-1]
        if(node.retFlag==0): #RX1
            print("in ret no. 0 for node",node.id)
            if(tx.received==1): #if tx received by atleast 1 gw
                 gwID = LrcDecision(tx)
                
                 node.bestgws.append(gwID) #debug
                              
                 if(env.now > main.bs[gwID].nextTx[tx.subband]):
                    print("in RX1 ACK")
                    if(main.bs[gwID].txchannelBusy[0]==1):
                        node.noAckReason[4]+=1 #tx channel busy due to ack
                        print("not ack due tx ch busy due to ack")
                        ans=0
                        
                    elif(main.bs[gwID].txchannelBusy[1]==1):
                        node.noAckReason[3]+=1 #tx channel busy due to beacon
                        print("not ack due tx ch busy due to beacon")
                        ans=0
                        
                    else:
                        #send ACK on RX1
                        #gw busy bw start and end time
                        print("ack sent for node",node.id,"on rx1 for frame",node.fcount)
                        main.bs[gwID].txchannelBusy[0]==1
                        node.AckSent[0]+=1 #on RX1 # stats
                        main.bs[gwID].nextTx[tx.subband]=env.now + 99*AckOnairTime
                        yield env.timeout(AckOnairTime)
                        main.bs[gwID].txchannelBusy[0]=0
                        
                        ans=1


                    #check if gwId bs already not txing on that 
                 else:
                    node.noAckReason[1]+=1 #duty cycle on g/g1
                    print("not ack due to duty cycle on g1/g")
                    ans=0
                 #end
     
            else:
                node.bestgws.append(-1)
                node.noAckReason[0]+=1 # not received by any gw
                ans =0
                print("no ack due to not received at any gw because of any reason!!") # tx channel[1] busy is the reason we are concerned about
                print(node.lost)
                
                
      

        
        else:
            print("in ret no. 1 for node",node.id) 
            if(tx.received==1): #if tx received by atleast 1 gw
                 gwID = LrcDecision(tx)
                
                 node.bestgws.append(gwID) 
                 print("rx2 called")
                
                 if(env.now > main.bs[gwID].nextTx[2]):
                    #check if gwId bs already not txing on 
                    print("in RX2 ACK")
                    if(main.bs[gwID].txchannelBusy[0]==1):
                        node.noAckReason[4]+=1 #tx channel busy due to ack
                        print("not ack due tx ch busy due to ack")
                        ans=0
                    elif(main.bs[gwID].txchannelBusy[1]==1):
                        node.noAckReason[3]+=1 #tx channel busy due to beacon
                        print("not ack due tx ch busy due to beacon")
                        ans=0
                    
                        
                        
                    else:
                        print("ack sent for node",node.id,"on rx2 for frame",node.fcount)
                        main.bs[gwID].txchannelBusy[0]=1
                        node.AckSent[1]+=1 #on RX2
                        main.bs[gwID].nextTx[2]=env.now + 9*AckOnairTime
                        yield env.timeout(AckOnairTime)
                        main.bs[gwID].txchannelBusy[0]=0
                        
                        ans=1


                 else:
              
                    node.noAckReason[2]+=1 #duty cycle on G3 due to beacon
                   
                    print("no ack due to duty cycle on G3")
                    ans=0
                    
                               
                    
                 
          
             
            else:
                node.bestgws.append(-1)
                node.noAckReason[0]+=1 # not received by any gw
                
                print("no ack due to not received at any gw because of any reason!!")
                print(node.lost)
                ans =0
              
      elif(AckFlag==0):
          ans=2
          print("unconfirmed tx") 
          node.frames.append(AckFlag)
         
      elif(AckFlag==2): #tx was not sent AckFlag==2
          print("tx was not sent",node.id,node.fcount)
          ans=3
       
      if(ans==1):
            print("got acknowledged",node.fcount)
            node.frames.append(AckFlag)
            node.fcount+=1
            node.nfcount = node.fcount +1
            node.retcount=0
                          
      elif(ans==0 and AckFlag==1):
             print("could not be acknowledged")    


def transmit(env,node,AckFlag,retFlag):
             
        tx = classes.transmission(node.id,env.now)
        tx.freq = random.randint(0,15)#([868.1,868.3,868.5,867.1,867.3,867.7,867.9,866.8,865.1,865.3,865.5,865.7,865.9,866.1,866.4,866.6])
        if(tx.freq==0 or tx.freq ==1 or tx.freq ==2):
               tx.subband =0 #G
        else:
               tx.subband =1 #G1
      

        if(env.now >= node.nextTx[tx.subband]):
            
             tx.fcount = node.fcount
             if(retFlag==1):
    
                node.retcount+=1 #total num of ret of a node
                                
                print("trying to send again",node.fcount,"ret attempt",node.retcount)
                node.globalretCount+=1
                tx.conf = 1
                tx.sf =12
                tx.cr =1 
                tx.bw =125
                tx.packetlen=node.packetlen
              
             else:

                print ("trying to send", node.fcount, "of node", node.id,"at",env.now)
                 
                tx.sf = random.randint(9,12)
                tx.cr = random.randint(1,4)
                tx.bw = random.choice([125, 250, 500])
                tx.packetlen = random.randint(8,40)
                node.packetlen=tx.packetlen 
               
                tx.conf = 0
                if(random.randint(1,100)< 10):
                    tx.conf=1
                if(tx.conf==1):
                    node.newConfUL+=1
             node.nfcount+=1
             node.sent+=1
            
               
             if(tx.conf ==1):  
                    print("confirmed tx")
                    node.confUL+=1
                    node.retTimeout=env.now+2000 #2sec
                    
                    AckFlag =1

             if(tx.conf==0):
                    print("Was unconfirmed tx")
                   
                    node.unconf+=1
                    AckFlag=0
                    node.fcount+=1

                    
             tx.sensitivity=getRxSens(tx.sf,tx.bw)
                
             tx.maxdist=maxDist(tx.sensitivity)
             print("maxDist", tx.maxdist)
            
             tx.sendTime = env.now
             timeOnAir = airtime(tx)
             #print(tx.packetlen,tx.sf,tx.bw,tx.cr,timeOnAir)
             #exit(-1)
             node.nextTx[tx.subband] =  99 * timeOnAir + env.now

             yield env.timeout(timeOnAir)
             tx.recTime = env.now
                
                    
                    # airtime is time it occupies the tx/rx channel

                
             
             for i in range(0,nrBS):
                        
                    gwpacket = classes.Packet(node,i,tx) #called after the tx reaches the gw
                     #dont need this since we are storing everthing required

                    if(gwpacket.lossFlag == 0):
                        tx.receivingGws.append(i)
                     
                        if(not(i in node.receivingGws)):
                            node.receivingGws.append(i)
                        
                        tx.rssiArr.append([gwpacket.rssi,i])
                    
                   

                     # lost at all gws due to tx channel busy due to beacons
             
             
                    global maxPrea
                    if(len(main.packetsAtBS[i])>=2):
                         if(main.packetsAtBS[i][-1].tx.recTime-main.packetsAtBS[i][-2].tx.recTime>maxPrea):
                                latestpack = main.packetsAtBS[i][-1]
                                main.packetsAtBS[i].clear()
                                main.packetsAtBS[i].append(latestpack)


                    tx.packetArr.append(gwpacket)
               
             if(len(tx.receivingGws)==0):
                 node.lossCount+=1
             if(tx.count2==nrBS):
                node.dataLoss[2]+=1
             if(tx.count0==nrBS):
                node.dataLoss[0]+=1
             if(tx.count1==nrBS):
                node.dataLoss[1]+=1
             if(tx.count3==nrBS):
                 node.dataLoss[3]+=1  
             
                                
             if(len(tx.receivingGws)==0):
                    tx.received = 0 # used for ACks # not received at any gateway
             else:
                    tx.received =1
                    
             node.txArr.append(tx)    
                     
        else:
                    print("end device duty cycle for node",node.id,"frame num",node.fcount)
                    node.EdDc+=1  
                    AckFlag =2   
               

        return AckFlag                  
                    
def maxDist(sensitivity):
    Ptx = 14 #dBm
    gamma = 2.08
    d0 = 40.0 # in meters
             
    Lpld0 = 127.41
   
    linkBudget = Ptx - sensitivity #toelarable path loss ;link-budeget ESP
    maxdist = d0/10*(math.e**((linkBudget-Lpld0)/(10.0*gamma))) # to get realistic nos
    return maxdist

# this function computes the airtime of a packet
# according to LoraDesignGuide_STD.pdf

def airtime(tx):
    H = 0        # implicit header disabled (H=0) or not (H=1)
    DE = 0       # low data rate optimization enabled (=1) or not (=0)
    Npream = 8   # number of preamble symbol (12.25  from Utz paper)

    if tx.bw == 125 and tx.sf in [11, 12]:
        # low data rate optimization mandated for BW125 with SF11 and SF12
        DE = 1
    

    Tsym = (2.0**tx.sf)/tx.bw
    Tpream = (Npream + 4.25)*Tsym
    payloadSymbNB = 8 + max(math.ceil((8.0*tx.packetlen-4.0*tx.sf+28+16-20*H)/(4.0*(tx.sf-2*DE)))*(tx.cr+4),0)
    Tpayload = payloadSymbNB * Tsym
    return Tpream + Tpayload


def LrcDecision(tx):
    
    maxrssi = max(tx.rssiArr, key = itemgetter(0))[1] 
    main.nodes[tx.nodeid].DLgwid= maxrssi # DL route for the node gets updated based on prev ULs
    return maxrssi


def checkcollision(packet,gwID,time): #packet is bs-node pair specific
    col=0
   
    if main.packetsAtBS[gwID]: #packet.bs is pointer to the "list" of packets at the bs, check if the list is non-empty
        #checking if the current packet collides with "ANY" packet at the bs
        #print("packetAtBS array is non-empty")
        
        for other in main.packetsAtBS[gwID]: #other pointer will iterate the list, the list of nodes
            
            #print("in coll",other.nodeid,packet.nodeid )
            if other.nodeid != packet.nodeid: # chcking for packets at a given bs which are from different nodes
               # simple collision
               
              
               if frequencyCollision(packet, other) \
                   and sfCollision(packet, other): #Checking collision bw the current packet and all other packets by all other nodes at the bs under question
                   #packet.bs to get the bsid , both sf and freq same--> collide
                   # if above conditions are true, then only differnt time can save!!, if either is false, the packets are anyway saved, doesnt matter they were sent simultaneously or not
                   
                       if timingCollision(packet, other,time):
                           # check who collides in the power domain
                           # same time, sf,freq- only saviour is capture effect, only one can be saved due to capture effect
                           c = powerCollision(packet, other) # c contains casualties

                           # follow function marks all the collided packets
                           # either this one, the other one, or both
                           for p in c:
                               #p.collided = 1
                               if p == packet: # if collided is the current
                                   col = True # packet collides only when freq, sf, time are same and power is lesser than the other
                                   
                       else:
                           # no timing collision, all fine
                           pass # null operation check for next packet 
                  
                       
                        
                       

        return col # after checking the current packet against all the packets at the bs
    return False # list of bs under question is empty, no collision chance , return 0



def frequencyCollision(p1,p2):
    if(p1.tx.freq==p2.tx.freq):
        #print("freq col!")
        return True
    else:
        #print("no freq col")
        return False

def sfCollision(p1, p2):
    if p1.tx.sf == p2.tx.sf:
        #print("sf col!")
        # p2 may have been lost too, will be marked by other checks
        return True
    else:
        #print("no sf col")
        return False

def powerCollision(p1, p2):
    powerThreshold = 6 # dB
    if abs(p1.rssi - p2.rssi) < powerThreshold:
        # packets are too close to each other, both collide
        # return both packets as casualties
        print("power col both lost")
        return (p1, p2)
    elif p1.rssi - p2.rssi < powerThreshold: # rssi is a neg no. smaller , the one with 6db lesser in absolute 
        # p2 overpowered p1, return p1 as casualty
        print("power col new packet lost")
        return (p1,)
    # p2 was the weaker packet, return it as a casualty
    else:
        print("power col other packet lost")
        return (p2,)

def timingCollision(p1, p2,time):
    # assuming p1 is the freshly arrived packet and this is the last check
    # we've already determined that p1 is a weak packet, so the only
    # way we can win is by being late enough (only the first n - 5 preamble symbols overlap)

    # assuming 8 preamble symbols
    Npream = 8

    # we can lose at most (Npream - 5) * Tsym of our preamble
    Tpreamb = 2**p1.tx.sf/(1.0*p1.tx.bw) * (Npream - 5)

    # check whether p2 ends in p1's critical section
    intArrTime = time - p2.sendTime #p1 arrives later
    toa_p2 = airtime(p2.tx)
    minGap = toa_p2 -Tpreamb
    #p2_end = p2.tx.sendTime + p2.tx.recTime
    #p1_cs = env.now + Tpreamb # p2 arived earlier in the env, p2 can overlap with only 3 symbols of the current packet p1; cs=critical section. p2 should end before 3 synbols of p1
    if intArrTime > minGap: # p2 overlap more than 3 synbols
        # p1 collided with p2 and lost
        print("same time col")
        return True
    else:
        print("diff times no col")
        return False # same freq and sf but different times, so no collision


        
def getRxSens(sf,bw):
   
    for i in range (1,7): #row
        if(sf == main.sensi[i][0]):
            for j in range(1,4): #cols
                if(bw == main.sensi[0][j]):
                     sensitivity = main.sensi[i][j]
                     return sensitivity






            

