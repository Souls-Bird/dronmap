import csv
import time
import random
import serial

x_value = 0
sender_1_rssi = 0
sender_2_rssi = 0
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

        csv_writer.writerow(info)
        print(x_value, sender_1_rssi, sender_2_rssi)

        x_value += 1
        parsedPacket = ser.readline().decode("utf-8").split("\t")
        if parsedPacket[0] == "SENDER1":
            sender_1_rssi = int(parsedPacket[2])
        elif parsedPacket[0] == "SENDER2":
            sender_2_rssi = int(parsedPacket[2])
        else:
            print("PACKET ERROR")

    time.sleep(1)
