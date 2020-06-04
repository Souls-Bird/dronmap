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
    mlat = x[0] - (dlat*100)
    dd_lat = dlat + float(mlat)/60

    dlon = int(str(x[1])[:1])
    mlon = x[1] - (dlon*100)
    dd_lon = dlon + float(mlon)/60

    return (dd_lat, dd_lon)

def evaluate_GPS_data(path, ax_lat, ax_lon):
    N = 500
    GPS_errors = []
    real_pos = [45.768869, 4.876695] #acording to maps, in Decimal Degrees
    latitude = np.array(pd.read_csv(path)["latitude"].tail(N))
    longitude = np.array(pd.read_csv(path)["longitude"].tail(N))
    mean_lat = mean(latitude)
    mean_lon = mean(longitude)
    stdev_lat = stdev(latitude)
    stdev_lon = stdev(longitude)

    x = np.arange(N)

    for i in range(N):
        error_GPS = haversine(real_pos, dm2dd([latitude[i], longitude[i]]), unit='m')
        GPS_errors.append(error_GPS)
        print(error_GPS)

    average_error = mean(GPS_errors)
    print("\n"+str(average_error))

    # gps1 = [latitude[1], longitude[1]]
    # print(gps1)
    # dist = haversine(dm2dd(gps1), real_pos, unit='m')
    # print(dist , "m")

    # ax_lat.plot(x, latitude, label="Latitude")
    # ax_lon.plot(x, longitude, label='Longitude')
    # ax_lat.errorbar(x, latitude, yerr=stdev_lat, label="Latitude")
    # ax_lon.errorbar(x, longitude, yerr=stdev_lon, label='Longitude')



if __name__ == "__main__":
    fig, (ax_lat, ax_lon) = plt.subplots(nrows=1, ncols=2, figsize=(18, 8))
    evaluate_GPS_data("./data/test5/1/data2.csv", ax_lat, ax_lon)
    fig.tight_layout()
    # plt.show()
