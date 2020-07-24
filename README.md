This repository is the work of Théotime BALAGUER on the research project "DRONMAP", led with the Agora team of Inria laboratory, in INSA Lyon, France.

## Python scripts

In the "Python" folder, you will find three groups of scripts :
- ***data_related_scripts*** : A succession of scripts used to harvest data from experiences and to analyze/visualize it
- ***Olympe_scripts*** : A set of classes that I used to learn how to fly a Parrot drone with the Olympe SDK
- ***experience_scripts*** : The scripts used for the real-world experiences

### data_related_scripts

Here is a bunch of tools used for data collection and analysis. There is also old versions of some of the scripts and all the data gathered during my internship (July 2020).

#### trace2.py
trace2 is the last-used class for visualization of the data. It should be used to plot the results of the experiments with drones.
It has tools to trace the evolution of RSSI, SNR or error rate for one LoRa sender and receiver.
Here is examples of what you can get :

![results_experience_6_to_17](/Python/images/exp6-17_Power_Inclinaison_comparison.png)
![results_experience_29_36_37](/Python/images/exp29-36+37_CR_experiment.png)


#### animate.py
Show the evolution of RSSI in real-time for 1 or 2 LoRa nodes.

Asks for a path where there is a .csv file and read in real time the fields "x_value" and "sender_rssi", and plot one against the other.

![animate_example](/Python/images/animate_example.png)

#### getData2.py and appendData.py
Save the data received on the MKRWAN1300 plugged to the computer into relevant folders. Experience is :
- 2 MKRWAN1300 sending packets at a fix distance from the receiver
- Each sender increases the sending power every N packets.
- Operator must change the **paths** (pathDataA, pathDataB, etc) and the value **N** directly in the code.

Functionning :

1. Detect a packet in the Serial interface **/dev/ttyACM0**
2. Read the field *NODE_NAME* of the incoming packet and save it in the file **pathDataA/data1.csv** or **pathDataA/data2.csv** if it is respectively **N1** or **N2**.
3. After saving **N** packets for each node, switches to **pathDataB** and create two new .csv files for saving.
4. Ends when all the defined paths are full.

appendData.py do the same job but doesn't erase the files. It simply append more data to the existing files. But the files must exist before execution of the program.

#### eval_GPS.py
Quick evaluation of the precision of the Ultimate GPS from Adafruit.

1. Operator change its current location and the number of points to keep directly in the code.
2. Read the fields *latitude* and *longitude* of the given .csv file.
3. Compute and plot the error in meters between the real position and the measured value with error bars.
4. Also compute the average error and the error between the average position and the real position.

![eval_GPS_example](/Python/images/eval_GPS_example.png)



### Olympe_scripts

Here is some Python scripts that I used to learn the [Olympe SDK](https://developer.parrot.com/docs/olympe/olympeapi.html). The best option is to use those scripts into the [Sphinx](https://developer.parrot.com/docs/sphinx/whatissphinx.html) simulation, before trying to fly a real drone.
I will not give more details about those classes as it is just examples of flying a drone.

### experience_scripts

Here is the Python scripts that I used to record data during experiments, along with all the data of the experiences with the drone (July 2020).

#### move_away.py and CR_record_move_away.py
These two programs allow to fly the drone and record the transmission data autonomously.

1. Operator launch the program with parameter *experience name*
2. He then provide
  - the number of seconds to hover at each step
  - the number of meters to go forward at each steps
  - the number of steps
  - the slope of the trajectory from the horizontal plane
  - (CR) the first CR
  - (CR) the second CR
3. The computer connect with the drone *via* Wifi and take-off.
4. When hovering, a new thread is created with the save_packets method and the data start to be recorded.
5. After all steps are done, get back to initial position and land.

## Arduino scripts

In the Arduino folder, you can find the programs that send and receive data with the Arduino MKRWAN1300 module.

### Transmitter

The programs **LoRa_sender, LoRa_sender_sensors and LoRa_sender_sensors_CR** are the three programs that I used on the sender nodes. The packet's fields are :
> [ NODE_NAME | PACKET_COUNTER | POWER | SF | CR | LATITUDE | LAT | LONGITUDE | LON | TEMPERATURE | PRESSURE | HUMIDITY | ALTITUDE | RSSI | SNR]

- **LoRa_sender** is the most basic and can run with the MKRWAN1300 only. It sends fake data and is used or testing purpose.
- **LoRa_sender_sensors** include the BME680 sensor breakout and et Ultimate GPS from Adafruit. The code is explicitly separated in three parts : [LoRa], [BME680], [GPS] to make it easy to disable one of the parts by commenting/uncommenting parts of the code. It reads the values of the sensors and send the LoRa packets accordingly.
- **LoRa_sender_sensors_CR** is quite the same as LoRa_sender_sensors but swap the CR value for each packet, between one CR and another.

### Receiver

The receiver is really simple, it only detect the packets and forward everything to the Serial interface of the board. We try to keep the receiver as simple as possible to reduce the compute power needed on the node as we have a computer to do the job.
