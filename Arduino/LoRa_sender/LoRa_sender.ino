#include <SPI.h>
#include <LoRa.h>

int counter = 0;
int power = 0;
int N = 100; //number of packets to send with same power
int K = 1;

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
  LoRa.print("michel1\t");
  LoRa.print(counter);
  LoRa.endPacket();

  counter++;
  
  long randNum = random(800, 1200);
  delay(1700+randNum);
}
