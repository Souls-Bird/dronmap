#include <SPI.h>
#include <LoRa.h>

//[GPS] Initialisation ---------------------------------
#include <Adafruit_GPS.h>

// what's the name of the hardware serial port?
#define GPSSerial Serial1

// Connect to the GPS on the hardware port
Adafruit_GPS GPS(&GPSSerial);

// Set GPSECHO to 'false' to turn off echoing the GPS data to the Serial console
// Set to 'true' if you want to debug and listen to the raw GPS sentences
#define GPSECHO false

uint32_t timer = millis();

//[BME680] Initialisation ---------------------------------
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"

#define BME_SCK 13
#define BME_MISO 12
#define BME_MOSI 11
#define BME_CS 10

#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BME680 bme; // I2C
//Adafruit_BME680 bme(BME_CS); // hardware SPI
//Adafruit_BME680 bme(BME_CS, BME_MOSI, BME_MISO,  BME_SCK);

//[LoRa] Initialisation ---------------------------------
int N = 10; //number of packets to send with same power
int counter = 0;
int power = 14;
int K = 1;   //how many time we increased power
int SF = 7;  //Spreading factor [7;12]
int CR = 5;  //Coding rate (5 = 4/5) [5;8]
static unsigned nextInterval = 2500;

void setup() {
  Serial.begin(115200);
  //while (!Serial);

  Serial.println("LoRa Sender");

  //[LoRa] Setup ---------------------------------
  if (!LoRa.begin(869500000)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  LoRa.setTxPower(power);


  //[GPS] Setup ---------------------------------
  // 9600 NMEA is the default baud rate for Adafruit MTK GPS's- some use 4800
  GPS.begin(9600);
  // uncomment this line to turn on RMC (recommended minimum) and GGA (fix data) including altitude
  //GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  // uncomment this line to turn on only the "minimum recommended" data
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY);
  // For parsing data, we don't suggest using anything but either RMC only or RMC+GGA since
  // the parser doesn't care about other sentences at this time
  // Set the update rate
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ); // 1 Hz update rate
  // For the parsing code to work nicely and have time to sort thru the data, and
  // print it out we don't suggest using anything higher than 1 Hz

  // Request updates on antenna status, comment out to keep quiet
  //GPS.sendCommand(PGCMD_ANTENNA);

  delay(1000);

  // Ask for firmware version
  GPSSerial.println(PMTK_Q_RELEASE);

  //[BME680] Setup ---------------------------------
  if (!bme.begin()) {
    Serial.println("Could not find a valid BME680 sensor, check wiring!");
    while (1);
  }
  // Set up oversampling and filter initialization
  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
  bme.setPressureOversampling(BME680_OS_4X);
  bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
  bme.setGasHeater(320, 150); // 320*C for 150 ms
}

void loop() {

  //[LoRa] loop ---------------------------------
  // Increase the sending power of 3 dBm every N packets
  /*if(counter > N*K){
    power += 3;
    K++;
    LoRa.setTxPower(power);
    }*/

  //[GPS] loop ---------------------------------
  // read data from the GPS in the 'main loop'
  char c = GPS.read();
  // if you want to debug, this is a good time to do it!
  if (GPSECHO)
    if (c) Serial.print(c);
  // if a sentence is received, we can check the checksum, parse it...
  if (GPS.newNMEAreceived()) {
    // a tricky thing here is if we print the NMEA sentence, or data
    // we end up not listening and catching other sentences!
    // so be very wary if using OUTPUT_ALLDATA and trying to print out data
    Serial.println(GPS.lastNMEA()); // this also sets the newNMEAreceived() flag to false
    if (!GPS.parse(GPS.lastNMEA())) // this also sets the newNMEAreceived() flag to false
      Serial.println("Failed to parse NMEA sentence");
    return; // we can fail to parse a sentence in which case we should just wait for another
  }




  if (millis() - timer > nextInterval) {
    timer = millis(); // reset the timer
    nextInterval = 1500 + random(800, 1200);

    //[BME680] loop ---------------------------------
    if (! bme.performReading()) {
      Serial.println("Failed to perform reading :(");
      return;
    }

    Serial.print("Sending packet: ");
    Serial.println(counter);

    Serial.print("N2\t");
    Serial.print(counter);
    Serial.print("\t");
    Serial.print(power);
    Serial.print("\t");
    Serial.print(SF);
    Serial.print("\t");
    Serial.print(CR);
    Serial.print("\t");
    Serial.print(GPS.latitude, 4); Serial.print("\t"); Serial.print(GPS.lat);
    Serial.print("\t");
    Serial.print(GPS.longitude, 4); Serial.print("\t"); Serial.print(GPS.lon);
    Serial.print("\t");
    Serial.print(bme.temperature); // temperature in °C
    Serial.print("\t");
    Serial.print(bme.pressure / 100.0); // pressure in hPa
    Serial.print("\t");
    Serial.print(bme.humidity); // humidity in %
    Serial.print("\t");
    Serial.println(bme.readAltitude(SEALEVELPRESSURE_HPA)); // approximation of altitude in m

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
    LoRa.print(GPS.latitude, 4); LoRa.print("\t"); LoRa.print(GPS.lat);
    LoRa.print("\t");
    LoRa.print(GPS.longitude, 4); LoRa.print("\t"); LoRa.print(GPS.lon);
    LoRa.print("\t");
    LoRa.print(bme.temperature); // temperature in °C
    LoRa.print("\t");
    LoRa.print(bme.pressure / 100.0); // pressure in hPa
    LoRa.print("\t");
    LoRa.print(bme.humidity); // humidity in %
    LoRa.print("\t");
    LoRa.print(bme.readAltitude(SEALEVELPRESSURE_HPA)); // approximation of altitude in m
    LoRa.endPacket();

    counter++;
  }

}
