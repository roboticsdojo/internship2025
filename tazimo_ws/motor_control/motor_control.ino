#include <Encoder.h>

// ===== Motor Driver Pins =====
// Motor 1 (Right)
#define RPWM1 5
#define LPWM1 6
#define R_EN1 7
#define L_EN1 8

// Motor 2 (Left)
#define RPWM2 9
#define LPWM2 10
#define R_EN2 11
#define L_EN2 12

// ===== Encoder Configuration =====
Encoder enc1(2, 3);  // Only interrupt-capable encoder (MUST use these pins)
#define ENC2_A A0    // Polled encoder (non-interrupt)
#define ENC2_B A1

// ===== Competition Constants =====
const int BAUD_RATE = 115200;  // Maximize serial throughput
const int CONTROL_RATE = 50;   // Hz (20ms)
const int TICKS_PER_REV = 136; // Your encoder resolution
const float MAX_RPM = 1580.0;   // Adjust based on motor specs

// ===== PID Control =====
#include <PID_v1.h>
double pid1_in, pid1_out, pid1_setpoint;
double pid2_in, pid2_out, pid2_setpoint;
PID pidLeft(&pid1_in, &pid1_out, &pid1_setpoint, 1.0, 0.1, 0.05, DIRECT);
PID pidRight(&pid2_in, &pid2_out, &pid2_setpoint, 1.0, 0.1, 0.05, DIRECT);

// ===== Global Variables =====
volatile long enc2_count = 0;    // volatile for polled encoder
bool last_ENC2_A_state = LOW;
float speed1 = 0, speed2 = 0;    // Target speeds (-1.0 to 1.0)
unsigned long last_control_time = 0;
unsigned long last_encoder_time = 0;

void setup() {
  // Motor control pins
  pinMode(RPWM1, OUTPUT);
  pinMode(LPWM1, OUTPUT);
  pinMode(R_EN1, OUTPUT);
  pinMode(L_EN1, OUTPUT);
  pinMode(RPWM2, OUTPUT);
  pinMode(LPWM2, OUTPUT);
  pinMode(R_EN2, OUTPUT);
  pinMode(L_EN2, OUTPUT);

  // Enable motor drivers
  digitalWrite(R_EN1, HIGH);
  digitalWrite(L_EN1, HIGH);
  digitalWrite(R_EN2, HIGH);
  digitalWrite(L_EN2, HIGH);

  // Encoder pins
  pinMode(ENC2_A, INPUT_PULLUP);
  pinMode(ENC2_B, INPUT_PULLUP);

  // PID setup
  pidLeft.SetMode(AUTOMATIC);
  pidRight.SetMode(AUTOMATIC);
  pidLeft.SetSampleTime(20); // 50Hz
  pidRight.SetSampleTime(20);
  pidLeft.SetOutputLimits(-255, 255);
  pidRight.SetOutputLimits(-255, 255);

  Serial.begin(BAUD_RATE);
}

void loop() {
  unsigned long current_time = millis();

  // 1. Poll non-interrupt encoder at max rate
  pollEncoder2();

  // 2. Run control logic at fixed 50Hz interval
  if (current_time - last_control_time >= (1000 / CONTROL_RATE)) {
    // Handle serial commands
    if (Serial.available()) {
      processSerialCommands();
    }

    // Update motor control
    updateMotors();

    // Send encoder data (timestamp + counts)
    if (current_time - last_encoder_time >= 20) { // 50Hz encoder reporting
      sendEncoderData();
      last_encoder_time = current_time;
    }

    last_control_time = current_time;
  }
}

void pollEncoder2() {
  // Optimized polling with state tracking
  bool current_A = digitalRead(ENC2_A);
  if (current_A != last_ENC2_A_state) {
    enc2_count += (current_A == digitalRead(ENC2_B)) ? 1 : -1;
    last_ENC2_A_state = current_A;
  }
}

void processSerialCommands() {
  String cmd = Serial.readStringUntil('\n');
  cmd.trim();

  // Velocity command (format: "V<speed1>,<speed2>")
  if (cmd.startsWith("V")) {
    int comma_pos = cmd.indexOf(',');
    if (comma_pos != -1) {
      speed1 = cmd.substring(1, comma_pos).toFloat();
      speed2 = cmd.substring(comma_pos + 1).toFloat();
      
      // Convert to RPM for PID
      pid1_setpoint = speed1 * MAX_RPM;
      pid2_setpoint = speed2 * MAX_RPM;
    }
  }
 if (cmd == "REQ") {
  sendEncoderData();
  return;
 }
Serial.println("Received command: " + cmd);  
// Add other commands like PID tuning if needed
}

void updateMotors() {
  // Get current RPM (interrupt encoder)
  pid1_in = getRPM(enc1.read(), 0);
  
  // Get current RPM (polled encoder - less accurate)
  pid2_in = getRPM(enc2_count, 1);
  
  // Compute PID outputs
  pidLeft.Compute();
  pidRight.Compute();
  
  // Apply to motors with safety limits
  setMotor(RPWM1, LPWM1, (int)constrain(pid1_out, -255, 255));
  setMotor(RPWM2, LPWM2, (int)constrain(pid2_out, -255, 255));

Serial.print("Setpoint L: ");
Serial.print(pid1_setpoint);
Serial.print(" RPM, Input: ");
Serial.print(pid1_in);
Serial.print(" RPM, Output: ");
Serial.println(pid1_out);
}

void setMotor(int rpwm, int lpwm, int speed) {
  if (speed >= 0) {
    analogWrite(rpwm, speed);
    analogWrite(lpwm, 0);
  } else {
    analogWrite(rpwm, 0);
    analogWrite(lpwm, -speed);
  }
}

float getRPM(long encoder_ticks, int encoder_num) {
  static long last_ticks[2] = {0, 0};
  static unsigned long last_time[2] = {0, 0};
  
  unsigned long current_time = micros();
  float time_elapsed = (current_time - last_time[encoder_num]) / 1e6;
  
  // Handle timer overflow and first run
  if (time_elapsed <= 0 || last_time[encoder_num] == 0) {
    last_time[encoder_num] = current_time;
    last_ticks[encoder_num] = encoder_ticks;
    return 0.0;
  }
  
  long delta_ticks = encoder_ticks - last_ticks[encoder_num];
  float rpm = (delta_ticks / (float)TICKS_PER_REV) * (60.0 / time_elapsed);
  
  // Update state
  last_ticks[encoder_num] = encoder_ticks;
  last_time[encoder_num] = current_time;
  
  return rpm;
}

void sendEncoderData() {
  // Atomic serial write to prevent corruption
  noInterrupts();
  long e1 = enc1.read();
  long e2 = enc2_count;
  interrupts();
  
  Serial.print("E");
  Serial.print(e1);
  Serial.print(",");
  Serial.print(e2);
  Serial.println();
}

// #include <Encoder.h>

// // ===== Motor Driver Pins (YOUR CONFIGURATION) =====
// #define RPWM1 5 // Right PWM Motor 1
// #define LPWM1 6 // Left PWM Motor 1
// #define R_EN1 7 // Right Enable Motor 1
// #define L_EN1 8 // Left Enable Motor 1

// #define RPWM2 9  // Right PWM Motor 2
// #define LPWM2 10 // Left PWM Motor 2
// #define R_EN2 11 // Right Enable Motor 2
// #define L_EN2 12 // Left Enable Motor 2

// // ===== Encoder Pins =====
// Encoder enc1(2, 3); // Motor 1 encoder (interrupt pins)
// #define ENC2_A A0   // Motor 2 encoder (polled)
// #define ENC2_B A1

// // ===== Constants =====
// const int BAUD_RATE = 9600;

// const int CONTROL_RATE = 50; // Hz (20ms interval)

// // ===== Global Variables =====
// long enc2_count = 0;          // Motor 2 tick counter
// bool last_ENC2_A_state = LOW; // For ENC2 polling
// float speed1 = 0, speed2 = 0; // Motor speeds (-1.0 to 1.0)

// void setup()
// {
//     // Initialize motor control pins
//     pinMode(RPWM1, OUTPUT);
//     pinMode(LPWM1, OUTPUT);
//     pinMode(R_EN1, OUTPUT);
//     pinMode(L_EN1, OUTPUT);
//     pinMode(RPWM2, OUTPUT);
//     pinMode(LPWM2, OUTPUT);
//     pinMode(R_EN2, OUTPUT);
//     pinMode(L_EN2, OUTPUT);

//     // Enable motor drivers (always HIGH for BTS7960)
//     digitalWrite(R_EN1, HIGH);
//     digitalWrite(L_EN1, HIGH);
//     digitalWrite(R_EN2, HIGH);
//     digitalWrite(L_EN2, HIGH);

//     // Initialize encoder pins
//     pinMode(ENC2_A, INPUT);
//     pinMode(ENC2_B, INPUT);

//     Serial.begin(BAUD_RATE);
// }

// // void loop()
// // {
// //     static unsigned long last_control_time = 0;

// //     // 1. Poll non-interrupt encoder (ENC2)
// //     pollEncoder2();

// //     // 2. Run control logic at fixed interval
// //     if (millis() - last_control_time >= (1000 / CONTROL_RATE))
// //     {
// //         processSerialCommands();
// //         updateMotors();
// //         sendEncoderData();
// //         last_control_time = millis();
// //     }
// // }

// void loop() {
//   if (Serial.available()) {
//     String cmd = Serial.readStringUntil('\n');
//     cmd.trim();

//     if (cmd == "REQ") {
//       pollEncoder2();  // Update encoder count
//       sendEncoderData();
//     } else if (cmd.startsWith("V")) {
//       int comma_pos = cmd.indexOf(',');
//       if (comma_pos != -1) {
//         speed1 = cmd.substring(1, comma_pos).toFloat();
//         speed2 = cmd.substring(comma_pos + 1).toFloat();
//         updateMotors();
//       }
//     }
//   }
// }

// // Poll ENC2 (A0/A1) manually since not interrupt-capable
// void pollEncoder2()
// {
//     bool current_A = digitalRead(ENC2_A);
//     if (current_A != last_ENC2_A_state)
//     {
//         bool current_B = digitalRead(ENC2_B);
//         enc2_count += (current_A == current_B) ? 1 : -1;
//         last_ENC2_A_state = current_A;
//     }
// }

// // Handle incoming serial commands (from ROS)
// void processSerialCommands()
// {
//     if (Serial.available())
//     {
//         String cmd = Serial.readStringUntil('\n');
//         cmd.trim();

//         // Expected format: "V<speed1>,<speed2>" (e.g., "V0.5,-0.3")
//         if (cmd.startsWith("V"))
//         {
//             int comma_pos = cmd.indexOf(',');
//             if (comma_pos != -1)
//             {
//                 speed1 = cmd.substring(1, comma_pos).toFloat();
//                 speed2 = cmd.substring(comma_pos + 1).toFloat();
//             }
//         }
//     }
// }

// // Drive motors with speed range [-1.0, 1.0]
// void updateMotors()
// {
//     // Constrain speeds to valid range
//     speed1 = constrain(speed1, -1.0, 1.0);
//     speed2 = constrain(speed2, -1.0, 1.0);

//       // Motor 1 (convert -1.0->1.0 to PWM)
//     if (speed1 >= 0)
//     {
//         analogWrite(RPWM1, speed1 * 255);
//         analogWrite(LPWM1, 0);
//     }
//     else
//     {
//         analogWrite(RPWM1, 0);
//         analogWrite(LPWM1, -speed1 * 255);
//     }

//     // Motor 2 (inverted)
//     if (speed2 >= 0)
//     {
//     analogWrite(RPWM2, 0);
//     analogWrite(LPWM2, speed2 * 255);
//     }
//     else 
//     {
//     analogWrite(RPWM2, -speed2 * 255);
//     analogWrite(LPWM2, 0);
//     }

// }

// // Send encoder data to ROS (format: "E<ticks1>,<ticks2>\n")
// void sendEncoderData()
// {
//     //  Build and send full line atomically to prevent malformed messages
//     char buf[32];  // enough for something like "E-123456,7890\n"
//     snprintf(buf, sizeof(buf), "E%ld,%ld\n", enc1.read(), enc2_count);
//     Serial.print(buf);  // single atomic print
// }
