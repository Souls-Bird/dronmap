# ------------------------------------------------------
# Tested with Ubuntu 18.04.3 LTS and python 3.6.9
#
#
# ====== Program description ======
# This program is meant to visualize and analyse data collected with the getData2.py program.
# It uses library matplotlib to trace diagrams and figures showing results of the experience and breaking down a lot of points into more usable averaged data.
#
#
#
# contact : theotime.balaguer@insa-lyon.fr
# ------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from math import sqrt
import os
from haversine import haversine

#PARAMETERS
step_power = 3        # Power shift at each step of the experience, in dBm
step_distance = 12    # Distance shift at each experience, in meters.
N = 200               # Number of points for a given distance and sending power


# Return the mean of the given list
# INPUT: A list of numbers
# OUTPUT: The mean of the list's values
def mean(data):
    return sum(data) / len(data)

# Return the standard deviation of the given list
# INPUT: A list of numbers
# OUTPUT: The standard deviation of the list's values
def stdev(data):
    x = 0
    moyenne = mean(data)
    for val in data:
        x += pow(abs(val-moyenne), 2)
    etype = sqrt(x/len(data))
    return etype

# Return the error rate in % of a list (i.e. : give the percentage of missing packets in a serie of packets of size N)
# INPUT: A list of received packets on N sent packets
# OUTPUT: the error rate of the serie, in %.
def error_rate(data):
    error = ((N-len(data))/N)*100
    return error

# Read the raw data in multiple folders, compute and return mean and stdev for each serie and each node.
# INPUT: A list of paths to folders containing experience's data ['./data/exp1', './data/exp2', './data/exp3', ...]
# OUTPUT: A 3 dimensional list with this structure:
#[ [[mean1(exp1), mean1(exp2), ...], [mean2(exp1), mean2(exp2), ...]],
#  [[[stdev1(exp1), stdev1(exp2), ...], [stdev2(exp1), stdev2(exp2), ...]]
#  ]
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

# Read the raw data in multiple folders, compute and return error rates for each serie and each node
# INPUT: A list of paths to folders containing experience's data ['./data/exp1', './data/exp2', './data/exp3', ...]
# OUTPUT: A 3-dimensional list with this structure:
# [ [error_rate(exp1, node1), error_rate(exp2, node1), ...], [error_rate(exp1, node2), error_rate(exp2, node2), ...] ]
def read_errors(paths):
    errors1 = []
    errors2 = []

    for path in paths:
        dataNode1 = pd.read_csv(path+'/data1.csv')['x_value']
        dataNode2 = pd.read_csv(path+'/data2.csv')['x_value']
        errors1.append(error_rate(dataNode1))
        errors2.append(error_rate(dataNode2))
    return (errors1, errors2)

# This method is obsolete
# This method has been made to analyse distance and power shift at the same time
# The paths given should be distance related (ex: [./12m, ./24m, ./36m])
# Each distance folder should contain 5 folders named EXACTLY like this exemple : In ./12m folder: [ ./E1_0dB, ./E1_3dB, ...] In ./24m folder: [ ./E2_0dB, ./E2_3dB, ...]
# INPUT: A list of paths to folders containing experience's data ['./data/exp1', './data/exp2', './data/exp3', ...]
# OUTPUT: Two 2-dimensional arrays containing the means of all th series of the experience
# In line (first dimension) is the distance parameter
# In column (second dimension) is the power parameter
def read_complete(paths):
    complete_data1 = [[0 for x in range(len(os.listdir(paths[0])))] for y in range(len(paths))]
    complete_data2 = [[0 for x in range(len(os.listdir(paths[0])))] for y in range(len(paths))]
    i = 0

    for path_dist in paths:
        path_pow = [path_dist+'/E'+str(i+1)+'_'+str(step_power*k)+'dB' for k in range(5)]
        j = 0
        for path in path_pow:
            dataNode1 = pd.read_csv(path+'/data1.csv')['sender_rssi']
            dataNode2 = pd.read_csv(path+'/data2.csv')['sender_rssi']
            complete_data1[i][j] = mean(dataNode1)
            complete_data2[i][j] = mean(dataNode2)
            j += 1
        i += 1

    return (complete_data1, complete_data2)

# Trace the evolution of RSSI in function of the sending power for two sending nodes
# Each point is the average of N measurements to reduce uncertainties.
# Each point has error bars showing the confidence interval at 98% (meaning the "real" average of the N values has 98% chances to be in this interval)
# INPUT: A 2x2 array containing the list of means and stdev for each sender, a matplotlib.Axes object where to plot
# OUTPUT: Updates the matplotlib.Axes object with the wanted plots
def trace_averaged(data_mean_stdev, ax):
    avrg1 = data_mean_stdev[0][0]
    avrg2 = data_mean_stdev[0][1]
    yerr1 = 2.3263*data_mean_stdev[1][0]/sqrt(N)
    yerr2 = 2.3263*data_mean_stdev[1][1]/sqrt(N)
    #value 2.3263 found on http://wwwmathlabo.univ-poitiers.fr/~phan/downloads/enseignement/tables-usuelles.pdf
    #for alpha = 0.02

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

# Trace a bar chart showing error rates in function of sending power for two nodes
# INPUT: A 2x2 array containing the list of error rates for each sender, a matplotlib.Axes object where to plot
# OUTPUT: Updates the matplotlib.Axes object with the wanted bar chart
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

# Main method to open a matplotlib window and visualise the data.
# Create 8 graphs showing the RSSI evolution and the error rate for 4 different distances between transceiver and receiver
# NO INPUT, the paths are set in this method.
# OUTPUT: open window and show results
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

# This method is still in development
# Show the evolution of RSSI in function of both distance and power with a 3D graph
def trace_3D_rssi(complete_data, ax3D):
    power = np.arange(0, 13, step_power)
    distance = np.arange(12, 49, step_distance)
    X, Y = np.meshgrid(power, distance, sparse=True)
    myData = np.array(complete_data)
    ax3D.plot_surface(X, Y, myData)
    ax3D.set_xlabel('Sending Power (dBm)')
    ax3D.set_ylabel('Distance (m)')



if __name__ == "__main__":


    #EXEMPLE COMPUTE DISTANCE WITH GPS
    gps1 = [-83.2783726,34.398273645]
    gps2 = [0.0,0.0]
    distGPS = haversine(gps1, gps2, unit='m')
    print(str(distGPS)+" m")
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
