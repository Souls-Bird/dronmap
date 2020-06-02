#include <SPI.h>
#include <LoRa.h>

int N = 10; //number of packets to send with same power
int counter = 0;
int power = 0;
int K = 1;   //how many time we increased power
int SF = 7;  //Spreading factor [7;12]
int CR = 5;  //Coding rate (5 = 4/5) [5;8]
float latitude = 45.786237960462216;
float longitude = 4.879757987425819;

void setup() {
  Serial.begin(9600);
  //while (!Serial);

  Serial.println("LoRa Sender");

  if (!LoRa.begin(869500000)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  LoRa.setTxPower(power);
}

void loop() {

  if(counter > N*K){
    power += 3;
    K++;
    LoRa.setTxPower(power);
  }
  Serial.print("Sending packet: ");
  Serial.println(counter);

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

  counter++;
  
  long randNum = random(800, 1200);
  delay(1700+randNum);
}
