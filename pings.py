import Uplink
import main
import random
import classes
'''
DL ping process for each ED
'select best gw'
10% duty cycle limit check on G3 sub-band for the 'selected gw'
ping-slot open check 
set a prob for sending a DL ping per node or global
'''
pingProb=0.5 # gives an ides about the percentage of ping slots used


def pings(env,node,startTime,done): # LRC gets a chance to send DL ping every beacon period
    
        
    while(done): 
            if(random.random()<pingProb and env.now in node.pingSlots): 
                DLgw = main.bs[node.DLgwid] # current best gw for the node based on latest UL tx

                if(env.now> DLgw.nextTx[2]): #check duty cycle limit
                    tx = classes.transmission(node.id,env.now)
                    
                    tx.subband =2
                    tx.sf =9
                    tx.cr =1
                    tx.bw =125
                    tx.packetlen = random.randint(2,30)
                    DLgw.nextTx[2] = env.now + 9*Uplink.airtime(tx)
                    main.pingsSent+=1
                else: 
                    main.pingDelay+=1
            if(env.now >=startTime+122880):
                done=0
            yield env.timeout(30) # need to check for each "Possible" ping window out of 4096 window
        