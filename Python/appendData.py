import csv
import time
import random
import serial
import sys

#INITIALISATIONS
x_value = 0
sender_rssi = 0
old_N_1 = 0
old_N_2 = 0
N_packet_1 = -1
N_packet_2 = -1
K1 = 1
K2 = 1
ser = serial.Serial('/dev/ttyACM0')
print(ser.name)
pathDataA = './data/test3/1'
pathDataB = './data/test3/2'
pathDataC = './data/test3/3'
pathDataD = './data/test3/4'
pathDataE = './data/test3/5'
pathDataF = './data/test3/6'
myPaths = [pathDataA, pathDataB, pathDataC, pathDataD, pathDataE, pathDataF]
path1 = pathDataA
path2 = pathDataA
fieldnames = ["x_value", "sender_rssi"]
info = {
    "x_value": x_value,
    "sender_rssi": sender_rssi,
}
info2 = {
    "x_value": x_value,
    "sender_rssi": sender_rssi,
}


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

                if parsedPacket[0] == "michel1":
                    N_packet_1 = int(parsedPacket[1])
                    if N_packet_1 > old_N_1:
                        old_N_1 = N_packet_1
                        info["sender_rssi"] = int(parsedPacket[2])
                        info["x_value"] = N_packet_1
                        csv_writer1.writerow(info)
                        print("1 --->", info)
                    else:
                        print("doublon 1")

                elif parsedPacket[0] == "michel2":
                    N_packet_2 = int(parsedPacket[1])
                    if N_packet_2 > old_N_2:
                        old_N_2 = N_packet_2
                        info2["sender_rssi"] = int(parsedPacket[2])
                        info2["x_value"] = N_packet_2
                        csv_writer2.writerow(info2)
                        print("2 --->", info2)
                    else:
                        print("doublon 2")
                else:
                    print("PACKET NAME ERROR :", parsedPacket)

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

                if K1 == 100 and K2 == 100:
                    sys.exit()

            except UnicodeDecodeError:
                print("CORRUPTED PACKET (Decode Error)")

            except ValueError:
                print("CORRUPTED PACKET (Value Error)")



    time.sleep(1)