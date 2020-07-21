/*
This is the receiver code for an Arduino's MKR1300
We forward every packet received via LoRa wireless physical interface to the Serial interface that should be connected to a computer for saving and visualisaton.
It also adds the RSSI information to the end of the packet for each packet received.

CAREFUL: This is not a continuous receive mode, as MKR1300 doesn't support interruptions.
This means that if there is too much LoRa packets coming, and if the packets are too large, the inherent buffer of the MKR could overflow and
you may lose a whole lot of packets.
To cancel this problem, one should use a MKR1310 instead, with the LoRa_receiver_continuous.ino code.
*/

#include <SPI.h>
#include <LoRa.h>

void setup() {
  Serial.begin(9600);
  while (!Serial);

  Serial.println("LoRa Receiver");

  if (!LoRa.begin(869525000)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
}

void loop() {
  // try to parse packet
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    // received a packet
    //Serial.print("Received packet '");

    // read packet
    while (LoRa.available()) {
      Serial.print((char)LoRa.read());
    }

    // print RSSI of packet
    //Serial.print("' with RSSI ");
    Serial.print("\t");
    Serial.print(LoRa.packetRssi());
    Serial.print("\t");
    Serial.println(LoRa.packetSnr());
  }
}
