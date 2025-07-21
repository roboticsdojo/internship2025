#include <Wire.h>
#include <VL53L0X.h>

VL53L0X tof;

#define TRIG_PIN 2
#define ECHO_PIN 3

int pointCount = 0;
bool tofDetected = false;
bool usDetected = false;

void setup() {
  Serial.begin(9600);
  Wire.begin();

  // Ultrasonic
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // VL53L0X
  tof.init();
  tof.setTimeout(500);
  tof.startContinuous();
}

long readUltrasonicCM() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH);
  long distanceCm = duration * 0.034 / 2;
  return distanceCm;
}

void loop() {
  int tofDistance = tof.readRangeContinuousMillimeters();
  int usDistance = readUltrasonicCM();

  // ---------- TOF Object Detection ----------
  if (tofDistance < 300 && tofDistance > 0 && !tofDetected) {
    pointCount++;
    tofDetected = true;
    Serial.println("TOF: Object detected!");
  } else if (tofDistance >= 300 || tofDistance == 0) {
    tofDetected = false;
  }

  // ---------- Ultrasonic Object Detection ----------
  if (usDistance < 20 && usDistance > 0 && !usDetected) {
    pointCount++;
    usDetected = true;
    Serial.println("Ultrasonic: Object detected!");
  } else if (usDistance >= 20 || usDistance == 0) {
    usDetected = false;
  }

  // ---------- Output ----------
  Serial.print("Points: ");
  Serial.print(pointCount);
  Serial.print(" | TOF: ");
  Serial.print(tofDistance);
  Serial.print(" mm | Ultrasonic: ");
  Serial.print(usDistance);
  Serial.println(" cm");

  delay(100);
}
