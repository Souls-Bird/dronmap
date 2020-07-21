# ------------------------------------------------------
# Tested with Ubuntu 18.04.3 LTS and python 3.6.9
#
#
# ====== Program description ======
# This program evaluates the performance of a GPS sensor.
# To do so we read data saved in a .csv file and compute distance from the received point and the "real" point where the experience took place
# NB: I took the "real" GPS coordinates from Google Maps system, but this data could suffer a little drift compared to the "real real" position of the experiment
#
# We use matplotlib to plot the error in meters and it's uncertainties
# One should pay a particular attention to unit of GPS data, between degrees-minutes and decimal degrees
#
#
# contact : theotime.balaguer@insa-lyon.fr
# ------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
from haversine import haversine
from math import sqrt
import numpy as np

def mean(data):
    return sum(data) / len(data)

def stdev(data):
    x = 0
    moyenne = mean(data)
    for val in data:
        x += pow(abs(val-moyenne), 2)
    etype = sqrt(x/len(data))
    return etype

# Converts degrees-minutes GPS position to decimal-degrees GPS position
def dm2dd(x):
    dlat = int(str(x[0])[:2])
    mlat = float(str(x[0])[2:])
    dd_lat = dlat + mlat/60

    dlon = int(str(x[1])[:1])
    mlon = float(str(x[1])[1:])
    dd_lon = dlon + mlon/60

    return (dd_lat, dd_lon)

# Read the given folder (input: path, must lead to a .csv file with fieldnames "latitude" and "longitude") and trace the evolution of error distance in function of packet number
# It also computes the average error and give the average position and the error between average position and real position
def evaluate_GPS_data(path, ax):
    N = 390                             # number of values you want to keep, from the end of the values (to get rid of the first values when the GPS was not set-up)
    GPS_errors = []
    real_pos = [45.768763, 4.876561]    # Real position of the node, acording to maps, in Decimal Degrees
    latitude = np.array(pd.read_csv(path)["latitude"].tail(N))
    longitude = np.array(pd.read_csv(path)["longitude"].tail(N))
    mean_lat = mean(latitude)
    mean_lon = mean(longitude)
    mean_position_dd = dm2dd([mean_lat, mean_lon])
    x = np.arange(N)

    for i in range(N):
        print(dm2dd([latitude[i], longitude[i]]))
        error_GPS = haversine(real_pos, dm2dd([latitude[i], longitude[i]]), unit='m')
        GPS_errors.append(error_GPS)
        print(error_GPS)

    average_error = mean(GPS_errors)
    stdev_error = stdev(GPS_errors)
    print("\nAverage error on "+str(N)+" packet : "+str(average_error)+" m")
    print("Real position : "+str(real_pos)+"\nAverage position on "+str(N)+" packets : "+str(mean_position_dd))
    print("Error between average position and real position : "+str(haversine(real_pos, mean_position_dd, unit='m')))

    ax.errorbar(x, GPS_errors, yerr=stdev_error)
    ax.set_title("Position error of Adafruit's Ultimate GPS in m")
    ax.set_xlabel("packet number")
    ax.set_ylabel("error from fix coordinates from Google maps (m)")

if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.gca()
    evaluate_GPS_data("./data/eval_GPS_1/data2.csv", ax)
    fig.tight_layout()
    plt.show()
