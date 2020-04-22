import matplotlib
import matplotlib.pyplot as plt
import numpy as np


labels = ['All', 'p_0.5', 'p_0.1', 'DRF']
# Beaconless_time = [97.38, 294.4, 246.29, 128.42]
# Beaconless_energy = [16.19 , 23.39 , 19.56, 10.24]
#
# StarvedNodes=[15,0,0,0]

beacon_col=[186.9,138.4,39.8,72.7]
No_beacon=[1.7,3.65,76.75,33.7]
beacon_rec=[46.4,92.95,118.45,138.6]
BeaconSent =[140.39,70.11, 13.40, 20.65]
# beacons_total=[]


# delayedPings10 = [11,9,8]
# delayedPings50 = [50,30,22]

x = np.arange(len(labels))  # the label locations
width = 0.25  # the width of the bars

fig, ax = plt.subplots()
# rects1 = ax.bar(x-width/2, delayedPings10, width, label='10 % of ping slots utilized')
# rects2 = ax.bar(x +width/2, delayedPings50, width, label='50 % of ping slots utilized')

rects1 = ax.bar(x - width/4,beacon_col, width, label='Avg. Beacon Collisions per ED')
rects2 = ax.bar(x-width , No_beacon, width, label='Avg. No Beacons per ED')
rects3 = ax.bar(x + width, beacon_rec, width, label='Avg. Beacons Received per ED')
rects4 = ax.bar(x + width/4, BeaconSent, width, label='Total Beacons Sent(x10^2)')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Average Number')
#ax.set_title('Delayed pings as the network scales (% of ping slots utilized)')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)
autolabel(rects3)
autolabel(rects4)

fig.tight_layout()

plt.show()

