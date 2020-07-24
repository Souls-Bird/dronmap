# ------------------------------------------------------
# Tested with Ubuntu 18.04.3 LTS and python 3.6.9
#
#This is just a quick test of the serial library
#
# contact : theotime.balaguer@insa-lyon.fr
# ------------------------------------------------------

import serial
import numpy as np
import matplotlib.pyplot as plt
import time

NLIGNES = 20
i = 0
ser = serial.Serial('/dev/ttyACM0')
print(ser.name)
t0 = time.time()
t1 = 0

try:
    graph = int(input("Graphics ? (0:no ; 1:yes)"))
except ValueError:
    print("Please enter 0 or 1")

with open("data.txt", "w") as file:
    while t1 - t0 < 20:
        file.write(ser.readline().decode("utf-8"))
        t1 = time.time()

if graph:
    with open("data.txt", "r") as file:
        data = np.zeros((1,1))
        for line in file:
            data = np.append(data, int(line.split("\t")[1]))
            i = i+1
        print(data)
        plt.plot(data)
        plt.show()

print("Data saved")
