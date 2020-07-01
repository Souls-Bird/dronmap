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

# Trace the evolution of RSSI in function of the sending power for two sending nodes
# Each point is the average of N measurements to reduce uncertainties.
# Each point has error bars showing the confidence interval at 98% (meaning the "real" average of the N values has 98% chances to be in this interval)
# INPUT: A 2x2 array containing the list of means and stdev for each sender, a matplotlib.Axes object where to plot
# OUTPUT: Updates the matplotlib.Axes object with the wanted plots
def trace_averaged(paths, data_mean_stdev_length, FW, ax):
    print(data_mean_stdev_length)
    avrg = np.array(data_mean_stdev_length[0])
    stdev = np.array(data_mean_stdev_length[1])
    length = np.array(data_mean_stdev_length[2])
    yerr = 2.3263*stdev/np.sqrt(length)
    #value 2.3263 found on http://wwwmathlabo.univ-poitiers.fr/~phan/downloads/enseignement/tables-usuelles.pdf
    #for alpha = 0.02

    distances = np.arange(0, len(paths)*FW, FW)

    m1, b1 = np.polyfit(distances, avrg, 1)

    ax.errorbar(distances, avrg, yerr=yerr, label='Drone sender')
    ax.plot(distances, m1*distances + b1, '--')
    ax.set_xlabel('Distance from receiver (m)')
    ax.set_ylabel('RSSI averaged on ~50 packets (dBm)')
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
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=1, ncols=4, figsize=(22,5))

    path_exp1 = create_path('exp2')
    path_exp2 = create_path('exp3')
    path_exp3 = create_path('exp4')
    path_exp4 = create_path('exp5')

    data_exp1 = read_mean_stdev(path_exp1)
    data_exp2 = read_mean_stdev(path_exp2)
    data_exp3 = read_mean_stdev(path_exp3)
    data_exp4 = read_mean_stdev(path_exp4)

    trace_averaged(path_exp1, data_exp1, FW, ax1)
    trace_averaged(path_exp2, data_exp2, FW, ax2)
    trace_averaged(path_exp3, data_exp3, FW, ax3)
    trace_averaged(path_exp4, data_exp4, FW, ax4)

    ax1.set_title('Inclinaison = 0°')
    ax2.set_title('Inclinaison = 30°')
    ax3.set_title('Inclinaison = 60°')
    ax4.set_title('Inclinaison = 90°')


    fig.tight_layout()
    plt.show()
