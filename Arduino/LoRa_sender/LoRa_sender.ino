/*
This is an old version of LoRa_sender_sensors.ino, which can be used without the sensors because every data is hard-coded.
The program sends a LoRa packet every 2.7 seconds. Every N packets sent, it increases the sending power by 3 dBm. Procedure is repeated K times
(Anyway, there is a hardware limit to the sending power within the MKR1300 board. It can only get to 14 dBm.)
*/

#include <SPI.h>
#include <LoRa.h>

int N = 10; //number of packets to send with same power
int counter = 0;
int power = 0;
int K = 1;   //how many time we increased power
int SF = 7;  //Spreading factor [7;12]
int CR = 8;  //Coding rate (5 = 4/5) [5;8]
float latitude = 45.786237960462216;
float longitude = 4.879757987425819;

unsigned long t1;
unsigned long t2;

void setup() {
  Serial.begin(9600);
  //while (!Serial);

  Serial.println("LoRa Sender");

  if (!LoRa.begin(869500000)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  LoRa.setTxPower(power);
  LoRa.setCodingRate4(CR);
}

void loop() {

  /*if(counter > N*K){
    power += 3;
    K++;
    LoRa.setTxPower(power);
  }*/
  Serial.print("Sending packet: ");
  Serial.println(counter);

  t1 = millis();
  // send packet
  LoRa.beginPacket();
  LoRa.print("N2\t");
  LoRa.print(counter);
  LoRa.print("\t");
  LoRa.print(power);
  LoRa.print("\t");
  LoRa.print(SF);
  LoRa.print("\t");
  LoRa.print(CR);
  LoRa.print("\t");
  LoRa.print(latitude);
  LoRa.print("\t");
  LoRa.print(longitude);
  LoRa.endPacket();
  t2 = millis();
  Serial.print("Time on air : ");
  Serial.println(t2-t1);

  counter++;

  delay(2300);
}
