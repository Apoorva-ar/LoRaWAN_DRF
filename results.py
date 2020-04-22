import main
import classes
import coordinates
import Uplink
import Downlink
import os
import math
import numpy as np

# in main.py set RLFlag to 0

symbTime =(2.0**12)/125# (2.0**tx.sf)/tx.bw
selectedGws=[]
BGws=0
nrBS =60
TotalSent=0
coll=0
TotalLost=0
TotalBeaconLost=0
TotalConf=0
TotalRet=0
TotalRetBeacon=0
R1=0
R2=0
R3=0

TotalEnergy=0 #widening due beacon lost
TotalBeaconLessTime=0
beaconlessPeriod=0
globalMax=0
TotalRecBeacons=0
TotalBeaconCol=0
TotalNotReceived=0
starvedNodes=0
TotalPingSlots=0

for n in main.nodes:
    print("node num",n.id)
    print("sent",n.sent)
    TotalSent+=n.sent
    TotalPingSlots+=n.pingSlotCount
    TotalLost+= (math.floor(n.lost[0]/nrBS)+n.lost[1] +n.lost[2] + n.lost[3])
    TotalRet+=n.globalretCount
    coll+=n.lost[3]
   
   
    print("confirmed(includes new txs and all retransmissions)",n.confUL)
    TotalConf+=n.confUL
    print("unconfirmed",n.unconf)
    print("new confirmed txs",n.newConfUL)
    print("Total no. of retrasmissions",n.globalretCount)
    
   

    print("data lost",n.dataLoss)
   
    print("frames=",len(n.frames))
 
    print("Ack sent",n.AckSent)
   

    print("beacon colliding", n.beaconCollision)
    TotalBeaconCol+= n.beaconCollision
    print("beacon received",n.beaconReceived)
    TotalRecBeacons+=n.beaconReceived
    print("no beacons count",n.notReceived)
    TotalNotReceived+=n.notReceived
    print("beacon receiving array",n.receivingID)
    maxDiff=0
    if(len(n.receivingID)==0):
         n.beaconlessTime=2*60 # 2 hours then switch to class A
         n.maxDiff= 56 # max value for 2 hours beaconless operation
         n.ExtraEnergy+=(n.maxDiff-1)*16.95
    n.beaconlessTime=0
    for index in range (0,len(n.receivingID)):
        if(index==0):
            diff = n.receivingID[index]-0
            n.beaconlessTime+=(diff-1)*128/60
            n.ExtraEnergy+=(diff-1)*16.95
        else:
            diff = n.receivingID[index]-n.receivingID[index-1]
            n.ExtraEnergy+=(diff-1)*16.95
            n.beaconlessTime+=(diff-1)*128/60
        if(diff>n.maxDiff):
            n.maxDiff=diff
    if(n.maxDiff>=56):
            n.maxDiff=56
            n.ExtraEnergy+=(n.maxDiff-1)*16.95
            n.beaconlessTime=120
    print("maxDiff",n.maxDiff)
    #n.beaconlessTime=(n.maxDiff-1)*(128/60) #minutes
    if n.beaconlessTime>globalMax:
        globalMax=n.beaconlessTime #max beaconlessTime in the entire simulation
    if(len(n.receivingID)==0):
        starvedNodes+=1
   
    TotalEnergy+=n.ExtraEnergy
    TotalBeaconLessTime+=n.beaconlessTime
  
    print("best gws",n.bestgws,"length",len(n.bestgws))
    print("receivingGws",n.receivingGws)
    print("--------------------------------------")

EdPower=25 #mW 14dBm
avgULAirTime=1318.91 #ms 125kHz, cr=1, 20 payload, 8 preamble, sf=12, CRC and implicit header enabled

totalRetEnergy=EdPower*TotalRetBeacon*avgULAirTime/1000

print("collissions", coll)
print ("total Sent",TotalSent)

print(" total conf",TotalConf) # approx gives total ACKs sent
print("beacons sent", main.beaconCount)
for gwid in range(0,main.nrBS):
    print("gw sent, not sent beacons",main.bs[gwid].sent, main.bs[gwid].notSent)
    print("beacon index",main.bs[gwid].beaconIndex)
#network load = airtime* no. of packets    
L1=main.beaconCount*729.09
   
L2= TotalRetBeacon*1318.9 #no. of ret due to beacon, using an avg airtime for UL txs 
gp=(L1+L2)/1000
print("network load",gp) #network load due to beacons

beaconAirTime =1220.61 #17 bytes
gatewayPower= 50 # mW 17dBm

beaconEnergy = beaconAirTime * main.beaconCount * gatewayPower/1000
conf_ratio=(TotalConf/TotalSent)*100

input('Press Enter to continue ...')
pingRatio=(main.pingDelay/TotalPingSlots)*100

fname = "exp_results1"+".csv"
print (fname)
if os.path.isfile(fname):
    res = "\n" + str(main.nrNodes) + " ," +  str(TotalSent) + " ," +  str(TotalConf) +  " ," +  str(conf_ratio) +" ," +  str(main.p[0]) + ", " + str(TotalLost) +  " ," +  str(TotalRet)+ " ," +  str(TotalBeaconCol/main.nrNodes) +" ," +  str(TotalNotReceived/main.nrNodes) +" ," +  str(TotalRecBeacons/main.nrNodes) +" ," + str(TotalBeaconLessTime/main.nrNodes) + " ,"+ str(TotalEnergy/main.nrNodes) + " ," + str(starvedNodes)  + " ," +  str(globalMax) + " ," +  str(main.beaconCount)+" ," +  str(pingRatio)
else:
    res = " #nrNodes ,Total sent, Total confirmed, conf%, prob,Total lost,Total ret, Avg beacon col, Avg no beacons, Avg Rec Beacons, Avg Beaconless Time ,beaconless widen window energy,# nodes starved , beaconless Period(minutes),Total Beacons sent, percenatge of delayed pings\n"  +  str(main.nrNodes) +  " ," +  str(TotalSent) + " ," +  str(TotalConf)  + " ," +  str(conf_ratio)+ " ,"  +  str(main.p[0]) + ", " + str(TotalLost) + " ," +  str(TotalRet)+ " ,"  +  str(TotalBeaconCol/main.nrNodes) +" ," +  str(TotalNotReceived/main.nrNodes) +" ,"+  str(TotalRecBeacons/main.nrNodes) +" ,"+ str(TotalBeaconLessTime/main.nrNodes) +" ,"+ str(TotalEnergy/main.nrNodes)+ " ," + str(starvedNodes) + " ," +  str(globalMax) + " ," +  str(main.beaconCount)+ " ," +  str(pingRatio)
with open(fname, "a") as myfile:
    myfile.write(res)
myfile.close()

print("activated gateways in DRF",main.activatedSet)
for node in main.nodes:
    print(node.threshold)
    print(node.receivingGws2)

exit(-1)
