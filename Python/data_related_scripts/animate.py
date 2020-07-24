# ------------------------------------------------------
# Tested with Ubuntu 18.04.3 LTS and python 3.6.9
#
# This is a short program to see RSSI evolution of two LoRa senders in real time.
# It asks for a path to a folder containing .../data1.csv and .../data2.csv and plots the RSSI evolution over the packet number.
# Has been made for development purpose.
#
# contact : theotime.balaguer@insa-lyon.fr
# ------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

path = input('Entrez le path des données à tracer : ')
double_node = int(input('2 transmetteurs ? (0:non 1:oui) : '))

def animate(i):
    data1 = pd.read_csv(path+'/packets.csv')
    data1 = data1.tail(500)
    x1 = data1['x_value']
    y1 = data1['sender_rssi']

    plt.cla()       #clear the axis

    plt.plot(x1, y1, label='Sender 1')
    plt.ylabel('RSSI')
    plt.xlabel('Packet Number')
    plt.legend(loc='upper left')
    plt.tight_layout()

def animate_2_nodes(i):
    data1 = pd.read_csv(path+'/data1.csv')
    data2 = pd.read_csv(path+'/data2.csv')
    data1 = data1.tail(500)
    data2 = data2.tail(500)
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

if double_node:
    ani = FuncAnimation(plt.gcf(), animate_2_nodes, interval=1000)
else:
    ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()
