import main
import math
import numpy as np
import Uplink

class transmission():
    def __init__(self,nodeid,time):
       
        self.nodeid = nodeid
        self.freq =0
        self.subband =0
        self.sf =0
        self.cr =0
        self.bw =0
        self.packetlen =0
        self.conf =0
        self.sensitivity =0
        self.sendTime=time
        self.recTime =0
        self.packetArr = []
        self.receivingGws = []
        self.received = 0
        self.mindist = 800
        self.nearestgw = -1
        self.rssiArr=[]
        self.fcount=0
        self.count0=0
        self.count1=0
        self.count2=0
        self.count3=0
       

class Packet(): # tells how a tx is received at a gw; is called when the packet is received at a gw
    def __init__(self,node,gwID,tx):
               
        Ptx = 14 #dBm
        gamma = 2.08
        d0 = 40.0 # in meters
        Lpld0 = 127.41
    

        self.nodeid=node.id
        self.tx=tx
        self.sendTime=tx.sendTime
        


        
        self.lossFlag = 0
        
        # log-shadow
        s=float(node.dist[gwID])/d0
        
        Lpl = Lpld0 + 10*gamma*math.log(s)
        Prx = Ptx - Lpl
        #print ("Prx",Prx,"sensi",tx.sensitivity)
        self.rssi=Prx
       
            

        if(node.dist[gwID] > tx.maxdist):
            if(tx.count0==0):
                node.lost[0] += 1 #number of gateways where the tx is lost due to Prx<sens
            self.lossFlag = 1
            tx.count0+=1
        if(not(gwID in node.receivingGws2)):
            if(node.dist[gwID]<= node.threshold):
            
                node.receivingGws2.append(gwID)
        if(main.bs[gwID].txchannelBusy[0]==1 ):
            if(tx.count1==0):
                node.lost[1] += 1
            self.lossFlag = 1
            tx.count1+=1
        if(main.bs[gwID].txchannelBusy[1]==1):
             
            if(tx.count2==0):
                node.lost[2] +=1
            tx.count2+=1
            self.lossFlag = 1
        if(self.lossFlag ==0): #if the packet reaches the gw then only makes sense to check for collision
            main.packetsAtBS[gwID].append(self) 

            if(Uplink.checkcollision(self,gwID,tx.sendTime)):
                if(tx.count3==0):
                    node.lost[3] +=1
                self.lossFlag =1
                tx.count3+=1
class myBS():
    def __init__(self, id,x,y):
        self.id = id
        self.x = x
        self.y = y
        self.beaconIndex=0
        self.sent=0
        self.notSent=0
        self.nextTx =[0,0,0] #G,G1,G3(Ack),G3(beacon) subbands
        self.activeFlag=0
        self.txchannelBusy=[0,0] #virtual channels=2; phy channels=1
        self.activateBeacon =0
        self.receivingED=[]
       
       
    
class myNode():
    def __init__(self, id, period,posx,posy):
        self.pingSlotCount=0
        self.pingSlots=[]
        self.pingPeriod=0
        self.pingProb=0 # not used as of now
        self.DLgwid=0    
        self.classB=0
        self.greedyMark=0
        self.pingNB=0 # takes value 2^0 to 2^7 i.e. 1 ping slot to 128 slots
        self.maxDiff=0
        self.ExtraEnergy=0
        self.beaconlessTime=0
        self.receivingID=[]
        self.beaconReceived=0
        self.beaconCollision=0
        self.notReceived=0
        self.receivingGws=[]
        self.receivingGws2=[]
        self.BufferTime=0
        self.id = id
        self.period = period
        self.fcount =1
        self.nfcount=2
        self.x = posx
        self.y = posy
        self.dist = []
        self.dist2 = []
        self.sent = 0
        self.confUL =0
        self.newConfUL=0
        self.retcount =0
        self.globalretCount=0
        self.unconf =0
        self.nextTx=[0,0]
        self.frames=[]
        self.bestgws=[]
        self.txArr=[]
        self.lost=[0,0,0,0]
        self.EdDc=0
        self.retTimeout=0
        self.dataLoss=[0,0,0,0]  # number of txs lost of a node due to beaconing
        self.lossCount=0
       
        self.prevLen=0
        self.noAckReason=[0,0,0,0,0,0]
        self.AckSent =[0,0] # on RX1 and Rx2
        self.mindist=800
        self.threshold=100
        self.greedyDist={}

        for i in range(0,main.nrBS):
            d = (np.sqrt((self.x-main.bs[i].x)*(self.x-main.bs[i].x)+(self.y-main.bs[i].y)*(self.y-main.bs[i].y)))/100
            d=d/10
            

            if(d<=self.mindist):
                self.mindist = d
                self.nearestgw=i
            self.dist.append(d)
            self.greedyDist[d]=i
            self.dist2.append([d,i])

        
     
        self.threshold= self.mindist
       
                


       
       
        



