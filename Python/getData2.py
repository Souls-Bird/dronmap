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

for path in myPaths:
    with open(path+'/data1.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
    with open(path+'/data2.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()


#PARAMETRES
N = 10 #Nombre de points pour une puissance, à une distance donnée

while True:
    with open(path1+'/data1.csv', 'a') as csv_file1:
        with open(path2+'/data2.csv', 'a') as csv_file2:

            csv_writer1 = csv.DictWriter(csv_file1, fieldnames=fieldnames)
            csv_writer2 = csv.DictWriter(csv_file2, fieldnames=fieldnames)

            #Récupération du paquet et découpage en tableau d'arguments
            try:
                parsedPacket = ser.readline().decode("utf-8").split("\t")
                print("\033[93m"+str(parsedPacket)+"\033[0m")
#PACKET = [ NODE_NAME | PACKET_COUNTER | POWER | SF | CR | LATITUDE | LAT | LONGITUDE | LON | TEMPERATURE | PRESSURE | HUMIDITY | ALTITUDE | RSSI ]
#UNITY = [ string | int | int | int | int | float | char | float | char | float(°C) | float(hPa) | float(%) | float(m) | int ]
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

                # if info['x_value'] >= K1*N:
                #     try:
                #         path1 = myPaths[K1]
                #         K1 += 1
                #     except IndexError:
                #         K1 = 100
                #         print('Index_error (1)')
                #
                #
                # if info2['x_value'] >= N*K2:
                #     try:
                #         path2 = myPaths[K2]
                #         K2 += 1
                #     except IndexError:
                #         K2 = 100
                #         print('Index_error (2)')
                #
                # if K1 == 100 and K2 == 100:
                #     print("Terminate experience")
                #     sys.exit()

            except UnicodeDecodeError:
                print("CORRUPTED PACKET (Decode Error)")

            except ValueError:
                print("CORRUPTED PACKET (Value Error)")

            except IndexError:
                print("CORRUPTED PACKET (Index Error)")



    time.sleep(1)
