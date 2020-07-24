# ------------------------------------------------------
# Tested with Ubuntu 18.04.3 LTS and python 3.6.9
#
# ====== Program description ======
# This program make it easy to visualize LoRa transmission data in different ways.
# The data should be stored in files with this architecture :
#
# -- data/
#     |-- experience_name/
#         |-- Distance_1/
#             |-- corrupted_packets.csv
#             |-- packets.csv
#         |-- Distance_2/
#             |-- corrupted_packets.csv
#             |-- packets.csv
#         |-- ...
#         |-- Distance_n/
#
# Where the distances folder are named as "NSTEP_DISTANCEm" (ex : 0_0m, 1_10m, 2_20m, ...) so that the folders keep ordered in an alphanumerical way
#

#
# contact : theotime.balaguer@insa-lyon.fr
# ------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from math import sqrt
import os


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
def error_rate(data, Nb_packets_without_errors):
    error = ((Nb_packets_without_errors-len(data))/Nb_packets_without_errors)*100
    return error

# Read the raw data in multiple folders, compute and return the average, standard deviation and length of each serie of values.
# INPUT: A list of paths to folders containing experience's data. ex : ['./data/exp1/0_0m', './data/exp1/1_10m', './data/exp1/2_20m', ...]
# OUTPUT: A tuple of 3 lists containing :
    # - the averaged value of the RSSI field of the data
    # - the standard deviation of these values
    # - The number of points that were used to create the average
def read_mean_stdev(paths):
    avrg_rssi = []
    stdev_rssi = []
    length_rssi = []

    for path in paths:
        dataNode = pd.read_csv(path+'/packets.csv')['sender_rssi']
        if len(dataNode) > 0:
            avrg_rssi.append(mean(dataNode))
            stdev_rssi.append(stdev(dataNode))
            length_rssi.append(len(dataNode))
        else:
            print("Fichier "+path+"/packets.csv vide.")
            avrg_rssi.append(0)
            stdev_rssi.append(0)
            length_rssi.append(0)

    return (avrg_rssi, stdev_rssi, length_rssi)


def read_snr(paths):
    avrg_snr = []
    stdev_snr = []
    length_snr = []

    for path in paths:
        dataSNR = pd.read_csv(path+'/packets.csv')['sender_snr']
        if len(dataSNR) > 0:
            avrg_snr.append(mean(dataSNR))
            stdev_snr.append(stdev(dataSNR))
            length_snr.append(len(dataSNR))
        else:
            print("Fichier "+path+"/packets.csv vide.")
            avrg_snr.append(0)
            stdev_snr.append(0)
            length_snr.append(0)

    return (avrg_snr, stdev_snr, length_snr)

# Read the raw data in multiple folders, compute and return error rates for each serie and each node
# INPUT: A list of paths to folders containing experience's data. ex : ['./data/exp1/0_0m', './data/exp1/1_10m', './data/exp1/2_20m', ...]
# INPUT: The theoretical number of packets that should have been received.
# OUTPUT: A 3-dimensional list with this structure:
# [ [error_rate(exp1, node1), error_rate(exp2, node1), ...], [error_rate(exp1, node2), error_rate(exp2, node2), ...] ]
def read_errors(paths, milliseconds, seconds):
    errors = []

    nb_packets_0m = 30000 / milliseconds        # First step last for 30 sec
    nb_packets = (seconds*1000) / milliseconds          # Change the 180000 value to SECONDS*1000 for each experience, divide by 2 for CR experiments

    print(nb_packets_0m)
    print(nb_packets)

    data_0m = pd.read_csv(paths[0]+'/packets.csv')['x_value']
    errors.append(error_rate(data_0m, nb_packets_0m))
    paths_copy = paths.copy()
    paths_copy.pop(0)

    for path in paths_copy:
        dataNode = pd.read_csv(path+'/packets.csv')['x_value']
        errors.append(error_rate(dataNode, nb_packets))
    return errors

# Trace the evolution of RSSI in function of the sending power for two sending nodes
# Each point is the average of N measurements to reduce uncertainties.
# Each point has error bars showing the confidence interval at 98% (meaning the "real" average of the N values has 98% chances to be in this interval)
# INPUT: A 2x2 array containing the list of means and stdev for each sender, a matplotlib.Axes object where to plot
# OUTPUT: Updates the matplotlib.Axes object with the wanted plots
def trace_averaged(paths, data_mean_stdev_length, FW, ax):
    # print(data_mean_stdev_length)
    avrg = np.array(data_mean_stdev_length[0])
    stdev = np.array(data_mean_stdev_length[1])
    length = np.array(data_mean_stdev_length[2])
    yerr = 2.3263*stdev/np.sqrt(length)
    #value 2.3263 found on http://wwwmathlabo.univ-poitiers.fr/~phan/downloads/enseignement/tables-usuelles.pdf
    #for alpha = 0.02

    distances = np.arange(0, len(paths)*FW, FW)

    m1, b1 = np.polyfit(distances, avrg, 1)

    ax.errorbar(distances, avrg, yerr=yerr)
    color = ax.get_lines()[-1].get_color()
    ax.plot(distances, m1*distances + b1, '--', color=color)
    ax.set_xlabel('Distance from receiver (m)')
    ax.set_ylabel('RSSI averaged on multiple packets (dBm)')
    ax.set_xticks(distances)
    ax.legend(loc='upper right')

def trace_snr(paths, data_snr, FW, ax):
    avrg_snr = np.array(data_snr[0])
    stdev_snr = np.array(data_snr[1])
    length = np.array(data_snr[2])
    yerr = 2.3263*stdev_snr/np.sqrt(length)

    distances = np.arange(0, len(paths)*FW, FW)

    m1, b1 = np.polyfit(distances, avrg_snr, 1)

    ax.errorbar(distances, avrg_snr, yerr=yerr)
    color = ax.get_lines()[-1].get_color()
    ax.plot(distances, m1*distances + b1, '--', color=color)
    ax.set_xlabel('Distance from receiver (m)')
    ax.set_ylabel("SNR averaged on multiple packets (dBm)")
    ax.set_xticks(distances)
    ax.legend(loc='upper right')

# Trace a bar chart showing error rates in function of sending power for two nodes
# INPUT: A 2x2 array containing the list of error rates for each sender, a matplotlib.Axes object where to plot
# OUTPUT: Updates the matplotlib.Axes object with the wanted bar chart
def trace_error(data_errors, data_errors2, FW, ax):

    distances = np.arange(0, len(data_errors)*FW, FW)
    width = 2

    #This is to show a small line in the bar chart when the error rate is below or equal to 0.
    for i in range(len(data_errors)):
        if data_errors[i] <= 0:
            data_errors[i] = 0.2
    for i in range(len(data_errors2)):
        if data_errors2[i] <= 0:
            data_errors2[i] = 0.2

    ax.bar(distances-width/2, data_errors,width=width, label='CR5')
    ax.bar(distances+width/2, data_errors2,width=width, label='CR8')
    ax.set_ylim(0, 100)
    ax.set_xlabel('Distance from receiver (m)')
    ax.set_ylabel('Error rate (%)')
    ax.set_xticks(distances)
    ax.legend(loc='upper left')

def create_path(experience_name):
    path = []
    radical_path = '../experience_scripts/data/'+experience_name+'/'
    for f in os.listdir(radical_path):
        path.append(radical_path+f)
    path.sort()
    return path

def results_experience_6_to_17():
    FW = 10
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=1, ncols=4, figsize=(19,5))

    # Creation of a list of paths leading to the raw data
    path_exp1 = create_path('exp6_pow3_d0')
    path_exp2 = create_path('exp7_pow3_d30')
    path_exp3 = create_path('exp8_pow3_d60')
    path_exp4 = create_path('exp9_pow3_d90')

    path_exp5 = create_path('exp10_pow8_d0')
    path_exp6 = create_path('exp11_pow8_d30')
    path_exp7 = create_path('exp12_pow8_d60')
    path_exp8 = create_path('exp13_pow8_d90')

    path_exp9 = create_path('exp14_pow13_d0')
    path_exp10 = create_path('exp15_pow13_d30')
    path_exp11 = create_path('exp16_pow13_d60')
    path_exp12 = create_path('exp17_pow13_d90')

    # Reading of the data contained in the paths and creation of a tuple (average, standard deviation, number of experiences (ie number of steps)) of three arrays
    data_exp1 = read_mean_stdev(path_exp1)
    data_exp2 = read_mean_stdev(path_exp2)
    data_exp3 = read_mean_stdev(path_exp3)
    data_exp4 = read_mean_stdev(path_exp4)

    data_exp5 = read_mean_stdev(path_exp5)
    data_exp6 = read_mean_stdev(path_exp6)
    data_exp7 = read_mean_stdev(path_exp7)
    data_exp8 = read_mean_stdev(path_exp8)

    data_exp9 = read_mean_stdev(path_exp9)
    data_exp10 = read_mean_stdev(path_exp10)
    data_exp11 = read_mean_stdev(path_exp11)
    data_exp12 = read_mean_stdev(path_exp12)

    # Trace the curves in the right place
    trace_averaged(path_exp1, data_exp1, FW, ax1)
    trace_averaged(path_exp2, data_exp2, FW, ax2)
    trace_averaged(path_exp3, data_exp3, FW, ax3)
    trace_averaged(path_exp4, data_exp4, FW, ax4)

    trace_averaged(path_exp5, data_exp5, FW, ax1)
    trace_averaged(path_exp6, data_exp6, FW, ax2)
    trace_averaged(path_exp7, data_exp7, FW, ax3)
    trace_averaged(path_exp8, data_exp8, FW, ax4)

    trace_averaged(path_exp9, data_exp9, FW, ax1)
    trace_averaged(path_exp10, data_exp10, FW, ax2)
    trace_averaged(path_exp11, data_exp11, FW, ax3)
    trace_averaged(path_exp12, data_exp12, FW, ax4)


    ax1.set_title('Slope = 0°')
    lines_ax1 = ax1.get_lines()
    ax1.legend((lines_ax1[0], lines_ax1[2], lines_ax1[4]) ,("Power = 3 dBm", "Power = 8 dBm", "Power = 13 dBm"))

    ax2.set_title('Slope = 30°')
    lines_ax2 = ax2.get_lines()
    ax2.legend((lines_ax2[0], lines_ax2[2], lines_ax2[4]) ,("Power = 3 dBm", "Power = 8 dBm", "Power = 13 dBm"))

    ax3.set_title('Slope = 60°')
    lines_ax3 = ax3.get_lines()
    ax3.legend((lines_ax3[0], lines_ax3[2], lines_ax3[4]) ,("Power = 3 dBm", "Power = 8 dBm", "Power = 13 dBm"))

    ax4.set_title('Slope = 90°')
    lines_ax4 = ax4.get_lines()
    ax4.legend((lines_ax4[0], lines_ax4[2], lines_ax4[4]) ,("Power = 3 dBm", "Power = 8 dBm", "Power = 13 dBm"))

    fig.tight_layout()
    plt.show()

def results_experience_29_36_37():
    FW = int(input("Meters forward ? : "))
    FW2 = int(input("Meters forward (2) ? : "))

    exp_name = 'exp29_CR5_d30'
    exp_name2 = 'exp30_CR8_d30'
    exp_name3 = 'exp36+37_CR5'
    exp_name4 = 'exp36+37_CR8'

    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18,12))
    path = create_path(exp_name)
    path2 = create_path(exp_name2)
    path3 = create_path(exp_name3)
    path4 = create_path(exp_name4)

    data_errors = read_errors(path, 2300, 120)
    data_errors2 = read_errors(path2, 2300, 120)
    data_errors3 = read_errors(path3, 2000, 180)
    data_errors4 = read_errors(path4, 2000, 180)

    data_rssi = read_mean_stdev(path)
    data_rssi2 = read_mean_stdev(path2)
    data_rssi3 = read_mean_stdev(path3)
    data_rssi4 = read_mean_stdev(path4)

    data_snr = read_snr(path)
    data_snr2 = read_snr(path2)
    data_snr3 = read_snr(path3)
    data_snr4 = read_snr(path4)

    trace_error(data_errors, data_errors2, FW, axes[0][0])
    trace_averaged(path, data_rssi, FW, axes[0][1])
    trace_averaged(path2, data_rssi2, FW, axes[0][1])
    trace_snr(path, data_snr, FW, axes[0][2])
    trace_snr(path2, data_snr2, FW, axes[0][2])

    trace_error(data_errors3, data_errors4, FW2, axes[1][0])
    trace_averaged(path3, data_rssi3, FW2, axes[1][1])
    trace_averaged(path4, data_rssi4, FW2, axes[1][1])
    trace_snr(path3, data_snr3, FW2, axes[1][2])
    trace_snr(path4, data_snr4, FW2, axes[1][2])

    lines_ax2 = axes[0][1].get_lines()
    axes[0][1].legend((lines_ax2[0], lines_ax2[2]) ,("CR=5", "CR=8"))

    lines_ax3 = axes[0][2].get_lines()
    axes[0][2].legend((lines_ax3[0], lines_ax3[2]) ,("CR=5", "CR=8"))

    lines_ax5 = axes[1][1].get_lines()
    axes[1][1].legend((lines_ax5[0], lines_ax5[2]) ,("CR=5", "CR=8"))

    lines_ax6 = axes[1][2].get_lines()
    axes[1][2].legend((lines_ax6[0], lines_ax6[2]) ,("CR=5", "CR=8"))

    # This is to show the row names
    rows = [exp_name.split('_')[0], exp_name3.split('_')[0]]
    pad = 5
    for ax, row in zip(axes[:,0], rows):
        ax.annotate(row, xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - pad, 0), xycoords=ax.yaxis.label, textcoords='offset points', size='large', ha='right', va='center')

    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    # results_experience_6_to_17()
    # results_experience_29_36_37()
