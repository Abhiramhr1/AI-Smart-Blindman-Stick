#include <SoftwareSerial.h>

SoftwareSerial espSerial(12, 13); // RX, TX

#define trig 9
#define echo 10
#define buz 11
const int touch = 7;
int transistorPin = 6;

void setup() {
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
  pinMode(buz, OUTPUT);
  pinMode(touch, INPUT); 
  Serial.begin(9600);
  espSerial.begin(115200);
  delay(2000);  // Set the baud rate for SoftwareSerial
  pinMode(transistorPin, OUTPUT); // Set transistor pin as output
}



void loop() {
  long distance = us();
  Serial.println(distance);
  if (distance <= 5) {
    espSerial.println("c");
    buzz();
    // if (Serial.available() > 0) {

    delayMicroseconds(400);
    if( distance < 100)
    {
      // Activate the vibrator for 1 second
      turnOnVibrator();
      tone(buz,5000,1000);
      delay(3000); // Wait for 1 second
      
      // Deactivate the vibrator for 1 second
      turnOffVibrator();
       // Wait for 1 second
    }
    else{
    delay(1000); // Add a delay to avoid continuous sending
    }


  }
  else{
    delay(100);
  }
  if(digitalRead(touch)){
    tone(buz,4000,5000);
  }
}

void turnOnVibrator() {
  digitalWrite(transistorPin, HIGH); // Set transistor pin to HIGH
}

void turnOffVibrator() {
  digitalWrite(transistorPin, LOW); // Set transistor pin to LOW
}

int us() {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);

 long t = pulseIn(echo, HIGH);
 return (t / 29) / 2;
}
void buzz()
{
tone(buz,5000,1000);
}
