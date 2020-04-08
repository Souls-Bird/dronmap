import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def animate(i):
    data = pd.read_csv('data.csv')
    x = data['x_value']
    y1 = data['sender_1_rssi']
    y2 = data["sender_2_rssi"]

    plt.cla()       #clear the axis

    plt.plot(x, y1, label='Sender 1')
    plt.plot(x, y2, label='Sender 2')
    plt.ylabel('RSSI')
    plt.xlabel('Packet Number')
    plt.legend(loc='upper left')
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()
