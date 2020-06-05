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

def dm2dd(x):
    dlat = int(str(x[0])[:2])
    mlat = float(str(x[0])[2:])
    dd_lat = dlat + mlat/60

    dlon = int(str(x[1])[:1])
    mlon = float(str(x[1])[1:])
    dd_lon = dlon + mlon/60

    return (dd_lat, dd_lon)

def evaluate_GPS_data(path, ax):
    N = 390
    GPS_errors = []
    real_pos = [45.768763, 4.876561] #acording to maps, in Decimal Degrees
    latitude = np.array(pd.read_csv(path)["latitude"].tail(N))
    longitude = np.array(pd.read_csv(path)["longitude"].tail(N))
    mean_lat = mean(latitude)
    mean_lon = mean(longitude)
    stdev_lat = stdev(latitude)
    stdev_lon = stdev(longitude)

    x = np.arange(N)

    for i in range(N):
        print(dm2dd([latitude[i], longitude[i]]))
        error_GPS = haversine(real_pos, dm2dd([latitude[i], longitude[i]]), unit='m')
        GPS_errors.append(error_GPS)
        print(error_GPS)

    average_error = mean(GPS_errors)
    stdev_error = stdev(GPS_errors)
    print("\n"+str(average_error))

    ax.errorbar(x, GPS_errors, yerr=stdev_error)

    # ax_lat.plot(x, latitude, label="Latitude")
    # ax_lon.plot(x, longitude, label='Longitude')
    # ax_lat.errorbar(x, latitude, yerr=stdev_lat, label="Latitude")
    # ax_lon.errorbar(x, longitude, yerr=stdev_lon, label='Longitude')

if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.gca()
    evaluate_GPS_data("./data/eval_GPS_1/data2.csv", ax)
    fig.tight_layout()
    plt.show()
