#include <Encoder.h>

// ===== Motor Driver Pins (YOUR CONFIGURATION) =====
#define RPWM1 5 // Right PWM Motor 1
#define LPWM1 6 // Left PWM Motor 1
#define R_EN1 7 // Right Enable Motor 1
#define L_EN1 8 // Left Enable Motor 1

#define RPWM2 9  // Right PWM Motor 2
#define LPWM2 10 // Left PWM Motor 2
#define R_EN2 11 // Right Enable Motor 2
#define L_EN2 12 // Left Enable Motor 2

// ===== Encoder Pins =====
Encoder enc1(2, 3); // Motor 1 encoder (interrupt pins)
#define ENC2_A A0   // Motor 2 encoder (polled)
#define ENC2_B A1

// ===== Constants =====
const int BAUD_RATE = 115200;
const int CONTROL_RATE = 50; // Hz (20ms interval)

// ===== Global Variables =====
long enc2_count = 0;          // Motor 2 tick counter
bool last_ENC2_A_state = LOW; // For ENC2 polling
float speed1 = 0, speed2 = 0; // Motor speeds (-1.0 to 1.0)

void setup()
{
    // Initialize motor control pins
    pinMode(RPWM1, OUTPUT);
    pinMode(LPWM1, OUTPUT);
    pinMode(R_EN1, OUTPUT);
    pinMode(L_EN1, OUTPUT);
    pinMode(RPWM2, OUTPUT);
    pinMode(LPWM2, OUTPUT);
    pinMode(R_EN2, OUTPUT);
    pinMode(L_EN2, OUTPUT);

    // Enable motor drivers (always HIGH for BTS7960)
    digitalWrite(R_EN1, HIGH);
    digitalWrite(L_EN1, HIGH);
    digitalWrite(R_EN2, HIGH);
    digitalWrite(L_EN2, HIGH);

    // Initialize encoder pins
    pinMode(ENC2_A, INPUT);
    pinMode(ENC2_B, INPUT);

    Serial.begin(BAUD_RATE);
}

void loop()
{
    static unsigned long last_control_time = 0;

    // 1. Poll non-interrupt encoder (ENC2)
    pollEncoder2();

    // 2. Run control logic at fixed interval
    if (millis() - last_control_time >= (1000 / CONTROL_RATE))
    {
        processSerialCommands();
        updateMotors();
        sendEncoderData();
        last_control_time = millis();
    }
}

// Poll ENC2 (A0/A1) manually since not interrupt-capable
void pollEncoder2()
{
    bool current_A = digitalRead(ENC2_A);
    if (current_A != last_ENC2_A_state)
    {
        bool current_B = digitalRead(ENC2_B);
        enc2_count += (current_A == current_B) ? 1 : -1;
        last_ENC2_A_state = current_A;
    }
}

// Handle incoming serial commands (from ROS)
void processSerialCommands()
{
    if (Serial.available())
    {
        String cmd = Serial.readStringUntil('\n');
        cmd.trim();

        // Expected format: "V<speed1>,<speed2>" (e.g., "V0.5,-0.3")
        if (cmd.startsWith("V"))
        {
            int comma_pos = cmd.indexOf(',');
            if (comma_pos != -1)
            {
                speed1 = cmd.substring(1, comma_pos).toFloat();
                speed2 = cmd.substring(comma_pos + 1).toFloat();
            }
        }
    }
}

// Drive motors with speed range [-1.0, 1.0]
void updateMotors()
{
    // Constrain speeds to valid range
    speed1 = constrain(speed1, -1.0, 1.0);
    speed2 = constrain(speed2, -1.0, 1.0);

      // Motor 1 (convert -1.0->1.0 to PWM)
    if (speed1 >= 0)
    {
        analogWrite(RPWM1, speed1 * 255);
        analogWrite(LPWM1, 0);
    }
    else
    {
        analogWrite(RPWM1, 0);
        analogWrite(LPWM1, -speed1 * 255);
    }

    // Motor 2 (inverted)
    if (speed2 >= 0)
    {
    analogWrite(RPWM2, 0);
    analogWrite(LPWM2, speed2 * 255);
    }
    else 
    {
    analogWrite(RPWM2, -speed2 * 255);
    analogWrite(LPWM2, 0);
    }

}

// Send encoder data to ROS (format: "E<ticks1>,<ticks2>")
void sendEncoderData()
{
    Serial.print("E");
    Serial.print(enc1.read()); // Motor 1 ticks (from Encoder lib)
    Serial.print(",");
    Serial.println(enc2_count); // Motor 2 ticks (polled)
}
