#include <SPI.h>
#include <LoRa.h>

int counter = 0;
int power = 14;
int SF = 7;  //Spreading factor [7;12]
int CR = 5;  //Coding rate (5 = 4/5) [5;8]
float latitude = 45.786237960462;
float longitude = 4.87975798742;
uint32_t timer = millis();
static unsigned nextInterval = 1000;
byte[] byteArray = [4];


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
  for (int i = 0; i < 4; i++) {
    byteArray[i] = (int)
    Serial.println();
  }

  /*
    if (millis() - timer > nextInterval) {
      timer = millis();
      Serial.print("Sending packet: ");
      Serial.println(counter);

      // send packet
      LoRa.beginPacket();
      LoRa.write(latitude);
      LoRa.print(latitude);
      LoRa.endPacket();

      counter++;

    }*/
}
