import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from math import sqrt

#PARAMETERS
path = './data/868_E1/E1_0dB'
step_power = 3

def mean(data):
    return sum(data) / len(data)

def stdev(data):
    x = 0
    moyenne = mean(data)
    for val in data:
        x += pow(abs(val-moyenne), 2)
    etype = sqrt(x/len(data))
    return etype

def read_data(paths):
    datas1 = []
    datas2 = []

    for path in paths:
        datas1.append(pd.read_csv(path+'/data1.csv').tail(N))
        datas2.append(pd.read_csv(path+'/data2.csv').tail(N))

    return (datas1, datas2)

#INPUT : un tableau de chemin vers les répertoires contenant les expériences ['./data/exp1', './data/exp2', './data/exp3', ...]
#OUTPUT : Un tuple 2x2 contenants les valeurs moyennes des données et leur écart type
#[ [[mean1(exp1), mean1(exp2), ...], [mean2(exp1), mean2(exp2), ...]],
#  [[[stdev1(exp1), stdev1(exp2), ...], [stdev2(exp1), stdev2(exp2), ...]]
#   ]
def read_mean_stdev(paths):

    avrg1 = []
    avrg2 = []
    yerr1 = []
    yerr2 = []

    for path in paths:
        dataNode1 = pd.read_csv(path+'/data1.csv')['sender_rssi']
        dataNode2 = pd.read_csv(path+'/data2.csv')['sender_rssi']
        avrg1.append(mean(dataNode1))
        avrg2.append(mean(dataNode2))
        yerr1.append(stdev(dataNode1))
        yerr2.append(stdev(dataNode2))
    return [[avrg1, avrg2], [yerr1, yerr2]]

def trace_averaged(data_mean_stdev, ax):
    avrg1 = data_mean_stdev[0][0]
    avrg2 = data_mean_stdev[0][1]
    yerr1 = data_mean_stdev[1][0]
    yerr2 = data_mean_stdev[1][1]

    power = np.arange(0, 13, step_power)

    # ax.plot(power, avrg1, label='Sender 1')
    # ax.plot(power, avrg2, label='Sender 2')
    ax.errorbar(power, avrg1, yerr=yerr1, label='Sender 1')
    ax.errorbar(power, avrg2, yerr=yerr2, label='Sender 2')
    ax.set_xlabel('Puissance d\'émission (dB)')
    ax.set_ylabel('moyenne RSSI sur 100 paquets')
    ax.legend(loc='upper left')

if __name__ == "__main__":

    data = ['./data/868_E1/E1_0dB', './data/868_E1/E1_3dB', './data/868_E1/E1_6dB', './data/868_E1/E1_9dB', './data/868_E1/E1_12dB']
    data2 = ['./data/868_E2/E2_0dB', './data/868_E2/E2_3dB', './data/868_E2/E2_6dB', './data/868_E2/E2_9dB', './data/868_E2/E2_12dB']

    fig, (ax, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16, 8))
    trace_averaged(read_mean_stdev(data2), ax)
    trace_averaged(read_mean_stdev(data), ax2)
    ax.set_title('Distance : 12 mètres')
    ax2.set_title('Distance : 24 mètres')
    fig.tight_layout()
    plt.show()
