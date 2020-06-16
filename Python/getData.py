# ----------------------------------------------------
# This is an old version of the acquisition program intended to receive data from the LoRa Receiver and store it into a csv file.
# 
# THIS VERSION SHOULD NOT BE USED, it is bugged, uncommented and was coded as a first draw. Please refer to getData2.py.
# ----------------------------------------------------

import csv
import time
import random
import serial

x_value = 0
sender_1_rssi = 0
sender_2_rssi = 0
old_N_1 = 0
old_N_2 = 0
N_packet_1 = -1
N_packet_2 = -1
ser = serial.Serial('/dev/ttyACM0')
print(ser.name)

fieldnames = ["x_value", "sender_1_rssi", "sender_2_rssi"]

with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:
    with open('data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "x_value": x_value,
            "sender_1_rssi": sender_1_rssi,
            "sender_2_rssi": sender_2_rssi
        }

        try:
            parsedPacket = ser.readline().decode("utf-8").split("\t")
        except UnicodeDecodeError:
            parsedPacket = "CORRUPTED PACKET"
            print("CORRUPTED PACKET")

        if parsedPacket[0] == "SENDER1":
            sender_1_rssi = int(parsedPacket[2])
            N_packet_1 = int(parsedPacket[1])
            x_value = N_packet_1
        elif parsedPacket[0] == "SENDER2":
            sender_2_rssi = int(parsedPacket[2])
            N_packet_2 = int(parsedPacket[1])
            x_value = N_packet_2
        else:
            print("PACKET NAME ERROR")

        #Gestion des doublons
        if N_packet_1 > old_N_1 or N_packet_2 > old_N_2:
            csv_writer.writerow(info)
            print(x_value, sender_1_rssi, sender_2_rssi)
            old_N_1 = N_packet_1
            old_N_2 = N_packet_2
        else:
            print("Doublon ou deja recu")

    time.sleep(1)
