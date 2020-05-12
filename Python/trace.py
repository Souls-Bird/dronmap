import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from math import sqrt
import os

#PARAMETERS
step_power = 3
step_distance = 12
N = 200

def mean(data):
    return sum(data) / len(data)

def stdev(data):
    x = 0
    moyenne = mean(data)
    for val in data:
        x += pow(abs(val-moyenne), 2)
    etype = sqrt(x/len(data))
    return etype


#INPUT : A list of received packets on N sent packets
#OUTPUT : the error rate of the serie, in %.
def error_rate(data):
    error = ((N-len(data))/N)*100
    return error

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

def read_errors(paths):
    errors1 = []
    errors2 = []

    for path in paths:
        dataNode1 = pd.read_csv(path+'/data1.csv')['x_value']
        dataNode2 = pd.read_csv(path+'/data2.csv')['x_value']
        errors1.append(error_rate(dataNode1))
        errors2.append(error_rate(dataNode2))
    return (errors1, errors2)

def read_complete(paths):
    complete_data1 = [[0 for x in range(len(os.listdir(paths[0])))] for y in range(len(paths))]
    complete_data2 = [[0 for x in range(len(os.listdir(paths[0])))] for y in range(len(paths))]
    i = 0

    for path_dist in paths:
        path_pow = [path_dist+'/E'+str(i+1)+'_'+str(3*k)+'dB' for k in range(5)]
        j = 0
        for path in path_pow:
            dataNode1 = pd.read_csv(path+'/data1.csv')['sender_rssi']
            dataNode2 = pd.read_csv(path+'/data2.csv')['sender_rssi']
            complete_data1[i][j] = mean(dataNode1)
            complete_data2[i][j] = mean(dataNode2)
            j += 1
        i += 1

    return (complete_data1, complete_data2)

def trace_averaged(data_mean_stdev, ax):
    avrg1 = data_mean_stdev[0][0]
    avrg2 = data_mean_stdev[0][1]
    yerr1 = data_mean_stdev[1][0]
    yerr2 = data_mean_stdev[1][1]

    npAvrg1 = np.array(avrg1)
    npAvrg2 = np.array(avrg2)

    power = np.arange(0, 13, step_power)

    m1, b1 = np.polyfit(power, npAvrg1, 1)
    m2, b2 = np.polyfit(power, npAvrg2, 1)

    # ax.plot(power, avrg1, label='Sender 1')
    # ax.plot(power, avrg2, label='Sender 2')
    ax.errorbar(power, avrg1, yerr=yerr1, label='Sender 1')
    ax.errorbar(power, avrg2, yerr=yerr2, label='Sender 2')
    ax.plot(power, m1*power + b1, '--')
    ax.plot(power, m2*power + b2, '--')
    ax.text(5, avrg1[2]+4,'m='+str(np.around(m1, decimals=2))+', b='+str(np.around(b1, decimals=2)))
    ax.text(5, avrg2[2]-4,'m='+str(np.around(m2, decimals=2))+', b='+str(np.around(b2, decimals=2)))
    ax.set_xlabel('Sending power (dBm)')
    ax.set_ylabel('RSSI averaged on 100 packets (dBm)')
    ax.set_xticks(power)
    ax.legend(loc='upper left')

def trace_error(data_errors, ax):
    errors1 = data_errors[0]
    errors2 = data_errors[1]

    power = np.arange(0, 13, step_power)

    ax.bar(power-0.8, errors1, label='Sender 1', align='edge')
    ax.bar(power, errors2, label='Sender 2', align='edge')
    ax.set_ylim(0, 100)
    ax.set_xlabel('Sending power (dB)')
    ax.set_ylabel('Error rate (%)')
    ax.set_xticks(power)
    ax.legend(loc='upper left')

def graphe_rssi_error():
    data = ['./data/868_E1/E1_0dB', './data/868_E1/E1_3dB', './data/868_E1/E1_6dB', './data/868_E1/E1_9dB', './data/868_E1/E1_12dB']
    data2 = ['./data/868_E2/E2_0dB', './data/868_E2/E2_3dB', './data/868_E2/E2_6dB', './data/868_E2/E2_9dB', './data/868_E2/E2_12dB']
    data3 = ['./data/868_E3/E3_0dB', './data/868_E3/E3_3dB', './data/868_E3/E3_6dB', './data/868_E3/E3_9dB', './data/868_E3/E3_12dB']
    data4 = ['./data/868_E4/E4_0dB', './data/868_E4/E4_3dB', './data/868_E4/E4_6dB', './data/868_E4/E4_9dB', './data/868_E4/E4_12dB']
    data5 = ['./data/868_E5/E5_0dB', './data/868_E5/E5_3dB', './data/868_E5/E5_6dB', './data/868_E5/E5_9dB', './data/868_E5/E5_12dB']


    fig, ((ax, ax2, ax3, ax4, ax5), (axb, ax2b, ax3b, ax4b, ax5b)) = plt.subplots(nrows=2, ncols=5, figsize=(18, 8))
    trace_averaged(read_mean_stdev(data), ax)
    trace_averaged(read_mean_stdev(data2), ax2)
    trace_averaged(read_mean_stdev(data3), ax3)
    trace_averaged(read_mean_stdev(data4), ax4)
    trace_averaged(read_mean_stdev(data5), ax5)
    ax.set_title('Distance : 12 mètres')
    ax2.set_title('Distance : 24 mètres')
    ax3.set_title('Distance : 36 mètres')
    ax4.set_title('Distance : 48 mètres')
    ax5.set_title('Distance : 60 mètres')
    trace_error(read_errors(data), axb)
    trace_error(read_errors(data2), ax2b)
    trace_error(read_errors(data3), ax3b)
    trace_error(read_errors(data4), ax4b)
    trace_error(read_errors(data5), ax5b)
    fig.tight_layout()
    plt.show()

def trace_3D_rssi(complete_data, ax3D):
    power = np.arange(0, 13, step_power)
    distance = np.arange(12, 49, step_distance)
    X, Y = np.meshgrid(power, distance, sparse=True)
    myData = np.array(complete_data)
    ax3D.plot_surface(X, Y, myData)
    ax3D.set_xlabel('Sending Power (dBm)')
    ax3D.set_ylabel('Distance (m)')



if __name__ == "__main__":

    graphe_rssi_error()
    # data5 = ['./data/868_E5/E5_0dB', './data/868_E5/E5_3dB', './data/868_E5/E5_6dB', './data/868_E5/E5_9dB', './data/868_E5/E5_12dB']
    #
    #
    # fig = plt.figure()
    # ax = fig.gca()
    # trace_averaged(read_mean_stdev(data5), ax)
    # plt.show()


    # fig = plt.figure(figsize=(14,8))
    # ax1 = fig.add_subplot(1,2,1,projection='3d')
    # ax2 = fig.add_subplot(1,2,2,projection='3d')
    # trace_3D_rssi(read_complete(['./data/868_E1', './data/868_E2', './data/868_E3', './data/868_E4'])[0], ax1)
    # trace_3D_rssi(read_complete(['./data/868_E1', './data/868_E2', './data/868_E3', './data/868_E4'])[1], ax2)
    # ax1.set_title('sender 1')
    # ax2.set_title('sender 2')
    # fig.tight_layout()
    # plt.show()
