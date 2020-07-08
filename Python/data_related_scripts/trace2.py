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
def error_rate(data):
    Nb_packets_without_errors = 15
    error = ((Nb_packets_without_errors-len(data))/Nb_packets_without_errors)*100
    return error

def read_mean_stdev(paths):
    avrg = []
    yerr = []
    length = []

    for path in paths:
        dataNode = pd.read_csv(path+'/packets.csv')['sender_rssi']
        avrg.append(mean(dataNode))
        yerr.append(stdev(dataNode))
        length.append(len(dataNode))

    return (avrg, yerr, length)

# Read the raw data in multiple folders, compute and return error rates for each serie and each node
# INPUT: A list of paths to folders containing experience's data ['./data/exp1', './data/exp2', './data/exp3', ...]
# OUTPUT: A 3-dimensional list with this structure:
# [ [error_rate(exp1, node1), error_rate(exp2, node1), ...], [error_rate(exp1, node2), error_rate(exp2, node2), ...] ]
def read_errors(paths):
    errors = []

    for path in paths:
        dataNode = pd.read_csv(path+'/packets.csv')['x_value']
        print(dataNode)
        errors.append(error_rate(dataNode))
    print(errors)
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
    ax.plot(distances, m1*distances + b1, '--')
    ax.set_xlabel('Distance from receiver (m)')
    ax.set_ylabel('RSSI averaged on ~50 packets (dBm)')
    ax.set_xticks(distances)
    ax.legend(loc='upper right')

# Trace a bar chart showing error rates in function of sending power for two nodes
# INPUT: A 2x2 array containing the list of error rates for each sender, a matplotlib.Axes object where to plot
# OUTPUT: Updates the matplotlib.Axes object with the wanted bar chart
def trace_error(data_errors, FW, ax):

    distances = np.arange(0, len(data_errors)*FW, FW)

    ax.bar(distances, data_errors, label='Sender 1', align='edge')
    ax.set_ylim(0, 100)
    ax.set_xlabel('Distance from receiver (m)')
    ax.set_ylabel('Error rate (%)')
    ax.set_xticks(distances)
    ax.legend(loc='upper left')

def create_path(experience_name):
    path = []
    radical_path = '../experience_code/data/'+experience_name+'/'
    for f in os.listdir(radical_path):
        path.append(radical_path+f)
    path.sort()
    return path

if __name__ == "__main__":

    FW = int(input("Meters forward ? : "))
    exp_name = input("Experience name ? : ")
    # fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=1, ncols=4, figsize=(22,5))
    #
    # # Creation of a list of paths leading to the raw data
    # path_exp1 = create_path('exp6_pow3_d0')
    # path_exp2 = create_path('exp7_pow3_d30')
    # path_exp3 = create_path('exp8_pow3_d60')
    # path_exp4 = create_path('exp9_pow3_d90')
    #
    # path_exp5 = create_path('exp10_pow8_d0')
    # path_exp6 = create_path('exp11_pow8_d30')
    # path_exp7 = create_path('exp12_pow8_d60')
    # path_exp8 = create_path('exp13_pow8_d90')
    #
    # path_exp9 = create_path('exp14_pow13_d0')
    # path_exp10 = create_path('exp15_pow13_d30')
    # path_exp11 = create_path('exp16_pow13_d60')
    # path_exp12 = create_path('exp17_pow13_d90')
    #
    # # Reading of the data contained in the paths and creation of a tuple (average, standard deviation, number of experiences (ie number of steps)) of three arrays
    # data_exp1 = read_mean_stdev(path_exp1)
    # data_exp2 = read_mean_stdev(path_exp2)
    # data_exp3 = read_mean_stdev(path_exp3)
    # data_exp4 = read_mean_stdev(path_exp4)
    #
    # data_exp5 = read_mean_stdev(path_exp5)
    # data_exp6 = read_mean_stdev(path_exp6)
    # data_exp7 = read_mean_stdev(path_exp7)
    # data_exp8 = read_mean_stdev(path_exp8)
    #
    # data_exp9 = read_mean_stdev(path_exp9)
    # data_exp10 = read_mean_stdev(path_exp10)
    # data_exp11 = read_mean_stdev(path_exp11)
    # data_exp12 = read_mean_stdev(path_exp12)
    #
    # # Trace the curves in the right place
    # trace_averaged(path_exp1, data_exp1, FW, ax1)
    # trace_averaged(path_exp2, data_exp2, FW, ax2)
    # trace_averaged(path_exp3, data_exp3, FW, ax3)
    # trace_averaged(path_exp4, data_exp4, FW, ax4)
    #
    # trace_averaged(path_exp5, data_exp5, FW, ax1)
    # trace_averaged(path_exp6, data_exp6, FW, ax2)
    # trace_averaged(path_exp7, data_exp7, FW, ax3)
    # trace_averaged(path_exp8, data_exp8, FW, ax4)
    #
    # trace_averaged(path_exp9, data_exp9, FW, ax1)
    # trace_averaged(path_exp10, data_exp10, FW, ax2)
    # trace_averaged(path_exp11, data_exp11, FW, ax3)
    # trace_averaged(path_exp12, data_exp12, FW, ax4)
    #
    #
    # ax1.set_title('Inclinaison = 0°')
    # lines_ax1 = ax1.get_lines()
    # ax1.legend((lines_ax1[0], lines_ax1[2], lines_ax1[4]) ,("Power = 3 dBm", "Power = 8 dBm", "Power = 13 dBm"))
    #
    # ax2.set_title('Inclinaison = 30°')
    # lines_ax2 = ax2.get_lines()
    # ax2.legend((lines_ax2[0], lines_ax2[2], lines_ax2[4]) ,("Power = 3 dBm", "Power = 8 dBm", "Power = 13 dBm"))
    #
    # ax3.set_title('Inclinaison = 60°')
    # lines_ax3 = ax3.get_lines()
    # ax3.legend((lines_ax3[0], lines_ax3[2], lines_ax3[4]) ,("Power = 3 dBm", "Power = 8 dBm", "Power = 13 dBm"))
    #
    # ax4.set_title('Inclinaison = 90°')
    # lines_ax4 = ax4.get_lines()
    # ax4.legend((lines_ax4[0], lines_ax4[2], lines_ax4[4]) ,("Power = 3 dBm", "Power = 8 dBm", "Power = 13 dBm"))

    fig = plt.figure()
    ax = fig.gca()
    path = create_path(exp_name)

    data_errors = read_errors(path)

    trace_error(data_errors, FW, ax)

    fig.tight_layout()
    plt.show()
