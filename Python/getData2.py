import csv
import time
import random
import serial

x_value = 0
sender_rssi = 0
old_N_1 = 0
old_N_2 = 0
N_packet_1 = -1
N_packet_2 = -1
ser = serial.Serial('/dev/ttyACM0')
pathData = './data/E3/E34'
print(ser.name)

fieldnames = ["x_value", "sender_rssi"]

with open(pathData+'/data1.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

with open(pathData+'/data2.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:
    with open(pathData+'/data1.csv', 'a') as csv_file1:
        with open(pathData+'/data2.csv', 'a') as csv_file2:

            csv_writer1 = csv.DictWriter(csv_file1, fieldnames=fieldnames)
            csv_writer2 = csv.DictWriter(csv_file2, fieldnames=fieldnames)

            info = {
                "x_value": x_value,
                "sender_rssi": sender_rssi,
            }

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
                        info["sender_rssi"] = int(parsedPacket[2])
                        info["x_value"] = N_packet_2
                        csv_writer2.writerow(info)
                        print("2 --->", info)
                    else:
                        print("doublon 2")
                else:
                    print("PACKET NAME ERROR :", parsedPacket)

            except UnicodeDecodeError:
                print("CORRUPTED PACKET")
                continue

    time.sleep(1)
