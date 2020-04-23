import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def animate(i):
    data1 = pd.read_csv('./data/E4/data1.csv')
    data2 = pd.read_csv('./data/E4/data2.csv')
    data1 = data1.tail(40)
    data2 = data2.tail(40)
    x1 = data1['x_value']
    y1 = data1['sender_rssi']
    x2 = data2['x_value']
    y2 = data2["sender_rssi"]


    plt.cla()       #clear the axis

    plt.plot(x1, y1, label='Sender 1')
    plt.plot(x2, y2, label='Sender 2')
    plt.ylabel('RSSI')
    plt.xlabel('Packet Number')
    plt.legend(loc='upper left')
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()
