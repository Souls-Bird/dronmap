# ------------------------------------------------------
# Tested with Ubuntu 18.04.3 LTS, python 3.6.9 and Parrot Olympe 1.2.1
#
# ====== Test-bed description ======
# This program is intended to work with a Parrot ANAFI4K drone, equipped with a LoRa Atmospheric sensor.
# The LoRa Atmospheric sensor is composed of an Arduino MKR1300, an Adafruit Ultimate GPS and an Adafruit BME680 breakout
# For more information about the LoRa Atpmospheric sensor refer to file LoRa_sender_sensors
#
#====== Experience description ======
# The drone is remotely controled by Parrot's SDK Olympe via simple commands.
# The LoRa Atmospheric test-bed is independent from the drone and is programmed to continuously send LoRa Packets containing atmospheric data and GPS position.
# The drone flight-plan is a straight trajectory with wayting points to measure and save data.
# The user first set-up the flight plan by chosing the distance between each step, the waiting time at each step, the number of steps before end of experience
# an the slope of the trajectory from the ground (90° is vertical, 0° is horizontal).
# THERE IS NO VERIFICATION ACCORDING TO DRONE ENVIRONMENT SO IT IS USER'S DUTY TO CHECK THE VALUE OF THE FLIGHT PLAN TO NOT CRASH THE DRONE
# Experience can start and drone is taking-off.
# Drone's commands are going through Wifi channel, sensed data is flowing through LoRa channel.
# When the drone reach a measure point and enter hovering state, the base-station start recording the LoRa packets for the given waiting time.
# When finished, drone receive next moveBy command.
# At the end of experience, the drone is automatically going back to the take-off GPS point and land. Experience is finished.
#
# ====== Program description ======
# We use threading to separate drone commands and LoRa-related code.
# We first ask for flight-plan to user and create according folders into the /data folder.
# Then we connect to the drone via Olympe's SDK. If you want to test the code with Parrot's Shpinx simulator, use 10.202.0.1 to connect to virtual ethernet interface.
# To connect to the real drone, use 192.168.42.1
# Drone take-off and saving of the take-off position via Olympe commands
# A first measure point is set where the drone is standing.
# The measure point procedure is in thread "save_packets".
# It creates the .csv file with proper field names and start recording data coming through Serial interface '/dev/ttyACM0'
# At the end of the previously set waiting time, the thread finishes and the main program take-over and send the next moving command to the drone.
# When experience is finished, we use Olympe's command "moveTo" with the saved take-off position to get back to home.
#
# contact : theotime.balaguer@insa-lyon.fr
# ------------------------------------------------------


import sys
import threading
import time
import random
import os
import math

# Importation for the data saving
import csv
import serial

# Importations for drone controlling
import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing, NavigateHome, moveTo
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged, NavigateHomeStateChanged, moveToChanged
from olympe.enums.ardrone3.Piloting import MoveTo_Orientation_mode
from olympe.messages.ardrone3.GPSSettingsState import GPSFixStateChanged, HomeChanged

# save N packets into .csv files and finishes
# Creation of the csv files and initialisation of the field names.
# CAREFUL, this erases previously saved .../packets.csv if the path has not been changed.
def save_packets(seconds, path):
    # print("Starting thread:", threading.current_thread().name)
    print("Saving packets for "+ str(seconds) +" seconds in \""+path+"\"...")

    #INITIALISATIONS
    x_value = 0
    sender_power = 0
    sender_SF = 0
    sender_CR = 0
    # sender_latitude = 0
    # sender_lat = ''
    # sender_longitude = 0
    # sender_lon = ''
    sender_temperature = 0.0
    sender_pressure = 0.0
    sender_humidity = 0.0
    sender_altitude = 0.0
    sender_rssi = 0
    sender_snr = 0.0
    old_n = 0             # value of the last received packet number
    n_packet = -1         # value of the actual packet number
    K1 = 1
    ser = serial.Serial('/dev/ttyACM0')
    print(ser.name)


    fieldnames = ["x_value",
        "power",
        "SF",
        "CR",
        # "latitude", "lat",
        # "longitude", "lon",
        "temperature",
        "pressure",
        "humidity",
        "altitude",
        "sender_rssi",
        "sender_snr"]
    info = {
        "x_value": x_value,
        "power": sender_power,
        "SF": sender_SF,
        "CR": sender_CR,
        # "latitude": sender_latitude,
        # "lat": sender_lat,
        # "longitude": sender_longitude,
        # "lon": sender_lon,
        "temperature": sender_temperature,
        "pressure": sender_pressure,
        "humidity": sender_humidity,
        "altitude": sender_altitude,
        "sender_rssi": sender_rssi,
        "sender_snr": sender_snr,
    }

    with open(path+'/packets.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    start_time = time.time()
    current_time = start_time
    while current_time - start_time < seconds:
        current_time = time.time()
        with open(path+'/packets.csv', 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
# Get the packet from serial and parse it into list of values
# The LoRa packet must correspond to this :
# PACKET = [ NODE_NAME | PACKET_COUNTER | POWER | SF | CR | LATITUDE | LAT | LONGITUDE | LON | TEMPERATURE | PRESSURE | HUMIDITY | ALTITUDE | RSSI ]
# UNITY = [ string | int | int | int | int | float | char | float | char | float(°C) | float(hPa) | float(%) | float(m) | int ]
            try:
                parsedPacket = ser.readline().decode("utf-8").split("\t")
                print("\033[93m"+str(parsedPacket)+"\033[0m")
                if parsedPacket[0] == "N2":
                    n_packet = int(parsedPacket[1])
                    if n_packet > old_n:
                        old_n = n_packet
                        info["x_value"] = n_packet
                        info["power"] = int(parsedPacket[2])
                        info["SF"] = int(parsedPacket[3])
                        info["CR"] = int(parsedPacket[4])
                        # info["latitude"] = float(parsedPacket[5])
                        # info["lat"] = parsedPacket[6]
                        # info["longitude"] = float(parsedPacket[7])
                        # info["lon"] = parsedPacket[8]
                        info["temperature"] = float(parsedPacket[5])
                        info["pressure"] = float(parsedPacket[6])
                        info["humidity"] = float(parsedPacket[7])
                        info["altitude"] = float(parsedPacket[8])
                        info["sender_rssi"] = int(parsedPacket[-2])
                        info["sender_snr"] = float(parsedPacket[-1])

                        csv_writer.writerow(info)
                        print("1 --->", info)
                    else:
                        print("doublon")
                else:
                    print("PACKET NAME ERROR :", parsedPacket)

            except UnicodeDecodeError:
                print("CORRUPTED PACKET (Decode Error)")

            except ValueError:
                print("CORRUPTED PACKET (Value Error)")

            except IndexError:
                print("CORRUPTED PACKET (Index Error)")

    # print("Ending thread:", threading.current_thread().name)

if __name__ == "__main__":
    print("Starting thread:", threading.current_thread().name)
    experience_name = str(sys.argv[1])                  # User give the name o the experience before launching to prevent data collision
    seconds = int(input("Seconds at each step : "))     # Number of seconds to wait at each measure point (seconds)
    FW = int(input("Meters forward each step : "))      # Distance from one measure point to another (meters)
    N_STEPS = int(input("Number of steps : "))          # Number of steps before end of experience
    DIRECTION = int(input("Direction (in degrees) : ")) # Slope of the straight trajectory in degrees from  the ground (90° is vertical movement, 0° is horizontal movement)
    paths = []

    for i in range(N_STEPS):
        path = "./data/"+experience_name+"/"+str(i*FW)+"m"
        paths.append(path)
        if not os.path.exists(path):
            os.makedirs(path)
    print(paths)

    print("\n\n\n ----- Starting experience ----- \n\n\n")

    # 192.168.42.1 to connect to the real drone
    # 10.202.0.1 to connect to virtual Ethernet interface (Sphinx)
    with olympe.Drone("192.168.42.1") as drone:
        drone.connect()

        # Save the "home" position to be able to get back to it later
        # drone(GPSFixStateChanged(fixed=1, _timeout=10, _policy='check_wait')).wait()
        drone(GPSFixStateChanged(_policy="wait"))
        drone_home = drone.get_state(HomeChanged)
        print(drone_home)

        drone(
            TakeOff()
            >> FlyingStateChanged(state="hovering", _timeout=5)
        ).wait()
        print("\n\n\n -----TakeOff complete----- \n\n\n")

        saver = threading.Thread(target=save_packets, args=(45, paths[0]))
        saver.start()
        saver.join()

        for STEP in range(1, N_STEPS):

            print("Drone moving "+str(FW*math.cos(DIRECTION*math.pi/180))+" m forward and "+str(FW*math.sin(DIRECTION*math.pi/180))+" up.")

            drone(
                moveBy(FW*math.cos(DIRECTION*math.pi/180), 0, -FW*math.sin(DIRECTION*math.pi/180), 0)
                >> FlyingStateChanged(state="hovering", _timeout=5)
            ).wait()

            saver = threading.Thread(target=save_packets, args=(seconds, paths[STEP]))
            saver.start()
            saver.join()

        print("\n\n\n ---- Experience finished, Back to home ---- \n\n\n")

        drone(
            moveTo(drone_home['latitude'], drone_home['longitude'], drone_home['altitude'], MoveTo_Orientation_mode.NONE, 0.0)
            >> moveToChanged(status='DONE')
        ).wait()

        print("\n\n\n ---- Landing... ---- \n\n\n")

        drone(
            Landing()
        ).wait()

        print("\n\n\n ---- Drone landed ---- \n\n\n")

        #Leaving the with statement and disconnecting the drone.


    print("Ending thread:", threading.current_thread().name)
