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
pathData1 = './data/E3/data1.csv'
pathData2 = './data/E3/data2.csv'
print(ser.name)

fieldnames = ["x_value", "sender_rssi"]

with open(pathData1, 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

with open(pathData2, 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:
    with open(pathData1, 'a') as csv_file1:
        with open(pathData2, 'a') as csv_file2:

            csv_writer1 = csv.DictWriter(csv_file1, fieldnames=fieldnames)
            csv_writer2 = csv.DictWriter(csv_file2, fieldnames=fieldnames)

            info = {
                "x_value": x_value,
                "sender_rssi": sender_rssi,
            }

            #Récupération du paquet et découpage en tableau d'arguments
            try:
                parsedPacket = ser.readline().decode("utf-8").split("\t")
            except UnicodeDecodeError:
                print("CORRUPTED PACKET")


            if parsedPacket[0] == "SENDER1":
                N_packet_1 = int(parsedPacket[1])
                if N_packet_1 > old_N_1:
                    old_N_1 = N_packet_1
                    sender_rssi = int(parsedPacket[2])
                    x_value = N_packet_1
                    csv_writer1.writerow(info)
                    print("1 --->", info)
                else:
                    print("doublon 1")

            elif parsedPacket[0] == "SENDER2":
                N_packet_2 = int(parsedPacket[1])
                if N_packet_2 > old_N_2:
                    old_N_2 = N_packet_2
                    sender_rssi = int(parsedPacket[2])
                    x_value = N_packet_2
                    csv_writer2.writerow(info)
                    print("2 --->", info)
                else:
                    print("doublon 2")
            else:
                print("PACKET NAME ERROR :", parsedPacket)


    time.sleep(1)
