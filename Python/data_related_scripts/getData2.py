# ------------------------------------------------------
# Tested with Ubuntu 18.04.3 LTS and python 3.6.9
#
# ====== Test-bed description ======
# This program is intended to work with three boards Arduino MKR1300.
# First and second boards are sending LoRa packets regularly and can be powered by independent source. --> Refer to Arduino/LoRa_sender_sensors.ino
# Third board is receiving LoRa packets and forwards every packet to the it's serial interface. --> Refer to Arduino/LoRa_receiver.ino
# Third board must be plugged to the computer running this code with USB port 0 (change string '/dev/ttyACM0' if plugged to another port)
#
# ====== Program description ======
# Read the Serial data flow coming from receiver MKR1300.
# Every packet is parsed into a list of values (separator inside LoRa packet is '\t', encoding is utf-8).
#
# Then, we read values NODE_NAME and PACKET_COUNTER to decide if and where we store the packet.
# We identify sender identity with the NODE_NAME value and store packets separately for each sender (files are |pathData|/data1.csv and |pathData|/data2.csv)
# Packets are sometimes received twice, so we check if the PACKET_COUNTER value is greater than the last received packet.
# In this case, we store the packet, otherwise, we throw it.
#
# We also store different sending power into different files. (THIS IS HARDCODED)
# You have to check at the sender side (LoRa_sender_sensors.ino) the number of packets sent with one sending power and make sure that the "N" value is corresponding.
# When the received packet is the last packet sent with the current power, we change the current saving file to the next value of the myPaths list.
#
# contact : theotime.balaguer@insa-lyon.fr
# ------------------------------------------------------

import csv
import time
import random
import serial
import sys

#INITIALISATIONS
x_value = 0
sender_power = 0
sender_SF = 0
sender_CR = 0
sender_rssi = 0
sender_latitude = 0
sender_lat = ''
sender_longitude = 0
sender_lon = ''
sender_temperature = 0.0
sender_pressure = 0.0
sender_humidity = 0.0
sender_altitude = 0.0
old_N_1 = 0
old_N_2 = 0
N_packet_1 = -1
N_packet_2 = -1
K1 = 1
K2 = 1
ser = serial.Serial('/dev/ttyACM0')
print(ser.name)

# Paths to the saving folder. Each folder should correspond to a given sending power. THESE FOLDERS MUST EXIST BEFORE EXECUTION
# Create more paths and expend myPaths list if you need more sending power.
pathDataA = './data/test5/1'
pathDataB = './data/test5/2'
pathDataC = './data/test5/3'
pathDataD = './data/test5/4'
pathDataE = './data/test5/5'
# pathDataF = './data/test3/6'
myPaths = [pathDataA, pathDataB, pathDataC, pathDataD, pathDataE]
path1 = pathDataA
path2 = pathDataA
fieldnames = ["x_value",
    "power",
    "SF",
    "CR",
    "latitude", "lat",
    "longitude", "lon",
    "temperature",
    "pressure",
    "humidity",
    "altitude",
    "sender_rssi"]
info = {
    "x_value": x_value,
    "power": sender_power,
    "SF": sender_SF,
    "CR": sender_CR,
    "latitude": sender_latitude,
    "lat": sender_lat,
    "longitude": sender_longitude,
    "lon": sender_lon,
    "temperature": sender_temperature,
    "pressure": sender_pressure,
    "humidity": sender_humidity,
    "altitude": sender_altitude,
    "sender_rssi": sender_rssi,
}
info2 = {
    "x_value": x_value,
    "power": sender_power,
    "SF": sender_SF,
    "CR": sender_CR,
    "latitude": sender_latitude,
    "lat": sender_lat,
    "longitude": sender_longitude,
    "lon": sender_lon,
    "temperature": sender_temperature,
    "pressure": sender_pressure,
    "humidity": sender_humidity,
    "altitude": sender_altitude,
    "sender_rssi": sender_rssi,
}

# Creation of the csv files and initialisation of the field names.
# CAREFUL, this erases previously saved .../data1.csv and .../data2.csv if the pathData has not been changed.
# You can use appendData.py if you want to continue a previous experience without losing the data.
for path in myPaths:
    with open(path+'/data1.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
    with open(path+'/data2.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()


#PARAMETRES
N = 10 # Number of points for one given sending power and distance /!\ this value must correpond to the value "N" of the files LoRa_sender_sensors.ino or LoRa_sender.ino

while True:
    with open(path1+'/data1.csv', 'a') as csv_file1:
        with open(path2+'/data2.csv', 'a') as csv_file2:

            csv_writer1 = csv.DictWriter(csv_file1, fieldnames=fieldnames)
            csv_writer2 = csv.DictWriter(csv_file2, fieldnames=fieldnames)

# Get the packet from serial and parse it into list of values
# The LoRa packet must correspond to this :
# PACKET = [ NODE_NAME | PACKET_COUNTER | POWER | SF | CR | LATITUDE | LAT | LONGITUDE | LON | TEMPERATURE | PRESSURE | HUMIDITY | ALTITUDE | RSSI ]
# UNITY = [ string | int | int | int | int | float | char | float | char | float(°C) | float(hPa) | float(%) | float(m) | int ]
            try:
                parsedPacket = ser.readline().decode("utf-8").split("\t")
                print("\033[93m"+str(parsedPacket)+"\033[0m")
                if parsedPacket[0] == "N1":
                    N_packet_1 = int(parsedPacket[1])
                    if N_packet_1 > old_N_1:
                        old_N_1 = N_packet_1
                        info["sender_rssi"] = int(parsedPacket[-1])
                        info["x_value"] = N_packet_1
                        info["power"] = int(parsedPacket[2])
                        info["SF"] = int(parsedPacket[3])
                        info["CR"] = int(parsedPacket[4])
                        info["latitude"] = float(parsedPacket[5])
                        info["lat"] = parsedPacket[6]
                        info["longitude"] = float(parsedPacket[7])
                        info["lon"] = parsedPacket[8]
                        info["temperature"] = float(parsedPacket[9])
                        info["pressure"] = float(parsedPacket[10])
                        info["humidity"] = float(parsedPacket[11])
                        info["altitude"] = float(parsedPacket[12])
                        csv_writer1.writerow(info)
                        print("1 --->", info)
                    else:
                        print("doublon 1")

                elif parsedPacket[0] == "N2":
                    N_packet_2 = int(parsedPacket[1])
                    if N_packet_2 > old_N_2:
                        old_N_2 = N_packet_2
                        info2["sender_rssi"] = int(parsedPacket[-1])
                        info2["x_value"] = N_packet_2
                        info2["power"] = int(parsedPacket[2])
                        info2["SF"] = int(parsedPacket[3])
                        info2["CR"] = int(parsedPacket[4])
                        info2["latitude"] = float(parsedPacket[5])
                        info2["lat"] = parsedPacket[6]
                        info2["longitude"] = float(parsedPacket[7])
                        info2["lon"] = parsedPacket[8]
                        info2["temperature"] = float(parsedPacket[9])
                        info2["pressure"] = float(parsedPacket[10])
                        info2["humidity"] = float(parsedPacket[11])
                        info2["altitude"] = float(parsedPacket[12])
                        csv_writer2.writerow(info2)
                        print("2 --->", info2)
                    else:
                        print("doublon 2")
                else:
                    print("PACKET NAME ERROR :", parsedPacket)

                # Changes the current path where each packet should be saved when we reach the last packet for one given power
                if info['x_value'] >= K1*N:
                    try:
                        path1 = myPaths[K1]
                        K1 += 1
                    except IndexError:
                        K1 = 100
                        print('Index_error (1)')

                if info2['x_value'] >= N*K2:
                    try:
                        path2 = myPaths[K2]
                        K2 += 1
                    except IndexError:
                        K2 = 100
                        print('Index_error (2)')

                # Kill the program if we reach the end of the myPaths list and stored all the data.
                if K1 == 100 and K2 == 100:
                    print("Terminate experience")
                    sys.exit()

            except UnicodeDecodeError:
                print("CORRUPTED PACKET (Decode Error)")

            except ValueError:
                print("CORRUPTED PACKET (Value Error)")

            except IndexError:
                print("CORRUPTED PACKET (Index Error)")



    time.sleep(1)
