import random
import math
import main
import pings

beaconAirTime =1220.61 # 17bytes payload frame 10 preamble, no CRC, no header (implicit mode)
def LRCbeaconIndex(env):
    while True:
        
        main.LRCIndex+=1
        yield env.timeout(128000)

def BeaconProcess(env,gw,p,startTime,finalFlag):  # beaconprocess of one of the selected gws
      
      while(True):
        gw.beaconIndex+=1
        
        if(env.now> gw.nextTx[2]  and gw.txchannelBusy[0]==0):
            if(random.random()<=p): #it will transmit  
                offset=random.random() # between 0 to 1ms
                gw.timestamp=env.now+offset # only offset determines whether there is a diff in arrival time of beacons by diff gws at a given node
            
                
                main.beaconCount+=1
                gw.activeFlag=1
                gw.sent+=1
             
                #print("beacon sent by gw",gw.id,"at time",env.now,"beaconNum", beaconCount)   
                gw.txchannelBusy[1] = 1
                yield env.timeout(5120) #beaconGuardTime+reservedTime
                gw.txchannelBusy[1] = 0
                
                gw.nextTx[2]= env.now + 9* beaconAirTime
                yield env.timeout(122880) 
                gw.activeFlag=0
            else:
            #print("missed beacon due to duty cycle")
                gw.notSent+=1
                yield env.timeout(128000)
        
        else:
            gw.notSent+=1
            main.beaconDelay+=1
            yield env.timeout(128000)

#check beacon col at each node
#called every beaconPeriod
#if two or more beacons reach the node with same power then a coll
#only randomness and power diff can save
#assuming all beaacons arrive at the same time 
def BeaconCol(node):
        actveBeacons=0 # to keep track that node doesnt receive any beacon in a beacon period then true is returned
        Ptx = 27 #dBm
        gamma = 2.08
        d0 = 40.0 # in meters
        Lpld0 = 127.41
        beaconRec=[]
       
        for gwID in node.receivingGws:
            if(main.bs[gwID].activeFlag==1): #the gw sent the beacon
                actveBeacons+=1

                s=float(node.dist[gwID])/d0
                Lpl = Lpld0 + 10*gamma*math.log(s)
                power = Ptx - Lpl
                beaconRec.append((main.bs[gwID].timestamp,power))
                
                if(len(beaconRec)>=2):
                        check=beaconRec[-1] #list (timestamp,power)
                    
                        if (check[1] - beaconRec[0][1])>6 :
                            #check is saved
                            beaconRec[0]=check
                            beaconRec.remove(check)
                        elif beaconRec[0][1] - check[1] > 6:
                            beaconRec.remove(check)
                            # prev is saved
                        else:
                            #todo power is almost same but maybe timeoffset is less than 1us then also demodulation is possible
                            
                            return 1 # coll ; in the calling fn increment node.beaconCollission
        if(actveBeacons!=0):
          return 0 # coll did not occur    
        else:
            return 2 # not col but no beacon reached the node in that beacon period



# list of gws through which beacon can reach the node
#check if the above gws sent the beacon 




def CheckBeaconCol(env, node):#Bgw is one of the gateways for which beaconing is activated
    
    while True:
        yield env.timeout(5120) # beacon actually sent 
        answer=-1
        
        answer=BeaconCol(node)
        if(answer==1):
            node.beaconCollision+=1
            

        elif(answer==0):
            node.beaconReceived+=1
            node.receivingID.append(main.LRCIndex) #beaconIndex is linked to LRC, so is common for all txing LLRs
            # node received the beacon, set pingNB
            if(node.classB==0): #first beacon locked  
                node.classB=1
                node.pingNB= 2**(random.randint(0,7))
                node.Pingperiod= (2**12/node.pingNB)*30
            

        elif(answer==2):
            node.notReceived+=1
            
        if(len(node.receivingID)!=0 and main.LRCIndex - node.receivingID[-1]>=55): #switch back to class A
                node.classB=0
                node.pingNB=0
                main.switchBack+=1
        if(node.classB): # if class B is on, update ping slot time "evry beacon window i.e after every 128 sec"
            node.pingSlots.clear()
            '''
             no. of windows in one period= 4096/node.pingNB
             each window is of 30 milli seconds
             random window in first period
            '''
            offset=random.randint(0,(4096/node.pingNB)) 
            node.pingSlots.append(env.now+offset*30) # env.now is when beacon has been transmitted
            node.pingSlotCount+=1
            for time in range(1,node.pingNB):
                 node.pingSlots.append(node.pingSlots[-1]+node.Pingperiod) 
                 time+=1
                 node.pingSlotCount+=1
            #print(node.pingNB,node.pingSlots)
            yield env.process(pings.pings(env, node,env.now,1))
        else:
            yield env.timeout(122880)
       
        