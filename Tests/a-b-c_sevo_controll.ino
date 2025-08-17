#include <Servo.h>

Servo myServo;

void setup() {
  Serial.begin(9600);       // Start serial communication
  myServo.attach(9);        // Attach the servo to pin 9
  Serial.println("Enter 'a'=0°, 'b'=90°, 'c'=180°");
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();

    if (command == 'a') {
      myServo.write(0);
      Serial.println("Moved to 0 degrees");
    } 
    else if (command == 'b') {
      myServo.write(90);
      Serial.println("Moved to 90 degrees");
    } 
    else if (command == 'c') {
      myServo.write(180);
      Serial.println("Moved to 180 degrees");
    } 
    else {
      Serial.println("Invalid command. Use 'a', 'b', or 'c'.");
    }

    delay(20); // Short delay for stability
  }
}
