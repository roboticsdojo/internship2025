x#include <Servo.h>           // Include Servo library

Servo myServo;              // Create a Servo object
char receivedChar;          // To store incoming Bluetooth command

void setup() {
  myServo.attach(9);        // Attach the servo to pin D9
  Serial.begin(9600);       // Begin hardware serial at 9600 baud rate
  Serial.println("Bluetooth Servo Ready"); // Send startup message
}

void loop() {
  // If HC-05 sends data (user sends via Bluetooth terminal)
  if (Serial.available()) {
    receivedChar = Serial.read();   // Read the incoming byte

    switch (receivedChar) {
      case 'a':
        myServo.write(0);           // Move to 0 degrees
        Serial.println("Servo moved to 0 degrees"); // Send feedback
        delay(1000);               // Wait for 20 seconds
        break;

      case 'b':
        myServo.write(90);          // Move to 90 degrees
        Serial.println("Servo moved to 90 degrees"); // Send feedback
        delay(1000);               // Wait for 20 seconds
        break;

      case 'c':
        myServo.write(180);         // Move to 180 degrees
        Serial.println("Servo moved to 180 degrees"); // Send feedback
        delay(1000);               // Wait for 20 seconds
        break;

      default:
        Serial.println("Invalid command. Use a, b, or c."); // Invalid input
        break;
    }
  }
}

