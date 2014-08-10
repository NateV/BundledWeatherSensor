/* This sketch will read DH11 Sensor data and write it via the Serial
Connection to a Raspberry Pi. 
*/

//include DHT library
#include "DHT.h"

//DHT Sensor Pins
#define DHTPIN 7
#define DHTTYPE DHT22

//Status LED pin
#define STATUS_LED 2

//Off button
#define OFF_BUTTON 13
int buttonState = 0;


//Create DHT instance
DHT dht(DHTPIN, DHTTYPE);


void setup(void) {
 //initialize DHT sensor
 dht.begin();
 pinMode(STATUS_LED, OUTPUT);
 pinMode(OFF_BUTTON, INPUT);
 
 //Blink twice for ON!
 blinkTimes(2, STATUS_LED);
 
 Serial.begin(9600);
 Serial.print("Starting....");
 Serial.print("Hi Raspberry Pi");
}

void loop(void) {
  //Read values from sensor
  buttonState = digitalRead(OFF_BUTTON);
  if(buttonState==HIGH) {
    float f_humidity = dht.readHumidity();
    float f_temp = dht.readTemperature();
 
    //convert to strings
    String s_humidity = String((int)f_humidity);
    String s_temp = String((int)f_temp);
  
    String request = "?temp=" + s_temp + "&humidity=" + s_humidity;
    Serial.println(request);
    blinkTimes(1, STATUS_LED);  
    delay(1000);
  } else {
    digitalWrite(STATUS_LED, HIGH)
    String request = "?TURN_OFF";
    Serial.println(request); 
    delay(1000);
  }
}



void blinkTimes(int times, int pin) {
  for (int i=0; i<times; i++) {
    digitalWrite(pin, HIGH);
    Serial.println("Blinking");
    delay(20);
    digitalWrite(pin,LOW);
    delay(50);
  } 
}
